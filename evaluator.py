def evaluate_file(input_path: str) -> list[dict]:
    # Create the output file path in the same directory as the input file
    output_path = build_output_path(input_path)

    results = []
    output_lines = []

    # Read all expressions from the input file
    with open(input_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Process one expression per line
    for line in lines:
        expr = line.rstrip("\n")

        # Dictionary for each expression
        entry = {
            "input": expr,
            "tree": "",
            "tokens": "",
            "result": ""
        }

        # First stage: tokenise the input and build the parse tree
        # If tokenising or parsing fails, tree/tokens/result = ERROR
        try:
            tokens = tokenize(expr)
            token_str = tokens_to_string(tokens)

            tree = parse(tokens)
            tree_str = tree_to_string(tree)

        except Exception:
            entry["tree"] = "ERROR"
            entry["tokens"] = "ERROR"
            entry["result"] = "ERROR"

            output_lines.append(f"Input: {expr}")
            output_lines.append("Tree: ERROR")
            output_lines.append("Tokens: ERROR")
            output_lines.append("Result: ERROR")
            output_lines.append("")

            results.append(entry)
            continue

        # Second stage: evaluate the valid parse tree
        # If evaluation fails, tree and tokens remain valid and only the result = ERROR
        try:
            result = evaluate_tree(tree)

            entry["tree"] = tree_str
            entry["tokens"] = token_str
            entry["result"] = float(result)

            output_lines.append(f"Input: {expr}")
            output_lines.append(f"Tree: {tree_str}")
            output_lines.append(f"Tokens: {token_str}")
            output_lines.append(f"Result: {format_result(result)}")

        except Exception:
            entry["tree"] = tree_str
            entry["tokens"] = token_str
            entry["result"] = "ERROR"

            output_lines.append(f"Input: {expr}")
            output_lines.append(f"Tree: {tree_str}")
            output_lines.append(f"Tokens: {token_str}")
            output_lines.append("Result: ERROR")

        # Add a blank line after each block
        output_lines.append("")
        results.append(entry)

    # Write the final output to output.txt
    with open(output_path, "w", encoding="utf-8") as file:
        file.write("\n".join(output_lines))

    return results

def build_output_path(input_path: str) -> str:
    # Build the path for output_q2.txt in the same folder as the input file
    import os
    return os.path.join(os.path.dirname(input_path), "output_q2.txt")


def tokenize(expr: str) -> list[tuple[str, str]]:
    # Convert the input string to list of tokens
    tokens = []
    i = 0
    n = len(expr)

    while i < n:
        c = expr[i]

        # Ignore whitespace
        if c.isspace():
            i += 1
            continue

        # Read a numeric literal
        if c.isdigit() or c == ".":
            start = i
            dot_count = 0

            while i < n and (expr[i].isdigit() or expr[i] == "."):
                if expr[i] == ".":
                    dot_count += 1
                    if dot_count > 1:
                        raise ValueError("Invalid number")
                i += 1

            number_text = expr[start:i]

            # Single dot alone is not a valid number
            if number_text == ".":
                raise ValueError("Invalid number")

            tokens.append(("NUM", number_text))
            continue

        # Read arithmetic operators
        if c in "+-*/":
            tokens.append(("OP", c))
            i += 1
            continue

        # Read opening parenthesis
        if c == "(":
            tokens.append(("LPAREN", c))
            i += 1
            continue

        # Read closing parenthesis
        if c == ")":
            tokens.append(("RPAREN", c))
            i += 1
            continue

        # Any other character is invalid
        raise ValueError("Invalid character")

    # Add an END token as the end of input
    tokens.append(("END", ""))
    return tokens

def parse(tokens: list[tuple[str, str]]):
    # Parse the token list using recursive descent
    pos = 0

    def current():
        # Return the current token
        return tokens[pos]

    # Take token if it matches
    def eat(expected_type=None, expected_value=None):
        nonlocal pos
        token = tokens[pos]

        if expected_type is not None and token[0] != expected_type:
            raise ValueError("Unexpected token")

        if expected_value is not None and token[1] != expected_value:
            raise ValueError("Unexpected token")

        pos += 1
        return token

    def parse_expression():
        node = parse_term()
        while current()[0] == "OP" and current()[1] in "+-":
            op = eat("OP")[1]
            right = parse_term()
            node = (op, node, right)

        return node

    def parse_term():
        node = parse_factor()
        while True:
            token = current()

            # Handle explicit multiplication and division
            if token[0] == "OP" and token[1] in "*/":
                op = eat("OP")[1]
                right = parse_factor()
                node = (op, node, right)

            # Handle implicit multiplication
            elif token[0] in ("NUM", "LPAREN"):
                right = parse_factor()
                node = ("*", node, right)

            else:
                break

        return node

    def parse_factor():
        token = current()

        # Unary negation is supported
        if token[0] == "OP" and token[1] == "-":
            eat("OP", "-")
            operand = parse_factor()
            return ("neg", operand)

        # Unary plus is not supported
        if token[0] == "OP" and token[1] == "+":
            raise ValueError("Unary + not allowed")

        return parse_primary()

    def parse_primary():
        token = current()

        if token[0] == "NUM":
            eat("NUM")
            return ("num", float(token[1]))
        # Opening and Closing parenthesis
        if token[0] == "LPAREN":
            eat("LPAREN")
            node = parse_expression()
            if current()[0] != "RPAREN":
                raise ValueError("Missing closing parenthesis")

            eat("RPAREN")
            return node

        raise ValueError("Unexpected token")

    # Start parsing
    tree = parse_expression()

    # Adding END after an expression
    if current()[0] != "END":
        raise ValueError("Extra input")

    return tree

#Converting tree
def tree_to_string(node) -> str:
    if node[0] == "num":
        value = node[1]
        return str(int(value)) if value.is_integer() else str(value)

    if node[0] == "neg":
        return f"(neg {tree_to_string(node[1])})"

    # Binary operations are printed as (op left right)
    op, left, right = node
    return f"({op} {tree_to_string(left)} {tree_to_string(right)})"


# Evaluate parse tree
def evaluate_tree(node) -> float:

    if node[0] == "num":
        return node[1]

    if node[0] == "neg":
        return -evaluate_tree(node[1])

    op, left, right = node
    left_value = evaluate_tree(left)
    right_value = evaluate_tree(right)

    if op == "+":
        return left_value + right_value
    if op == "-":
        return left_value - right_value
    if op == "*":
        return left_value * right_value
    if op == "/":
        if right_value == 0:
            raise ValueError("Division by zero")
        return left_value / right_value

    raise ValueError("Invalid operator")

# Converting the token list
def tokens_to_string(tokens: list[tuple[str, str]]) -> str:
    parts = []

    for token_type, value in tokens:
        if token_type == "END":
            parts.append("[END]")
        else:
            parts.append(f"[{token_type}:{value}]")

    return " ".join(parts)

#Whole number and non-whole number display
def format_result(value: float) -> str:
  
    if value.is_integer():
        return str(int(value))
    return f"{round(value, 4):.4f}".rstrip("0").rstrip(".")

# Run evaluator on input and display output
input_file = "/content/sample_input.txt"
results = evaluate_file(input_file)

with open("/content/output_q2.txt", "r", encoding="utf-8") as f:
    print(f.read())
    
