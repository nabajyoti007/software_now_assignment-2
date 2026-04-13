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
        # If evaluation fails, tree and tokens remain valid and only the result becomes ERROR
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
