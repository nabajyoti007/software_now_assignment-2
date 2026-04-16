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
