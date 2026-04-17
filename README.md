# software_now_assignment-2

## Overview
This repository contains solutions for HIT137 Group Assignment 2:

- Question 1: File Encryption and Decryption Program  
- Question 2: Mathematical Expression Evaluator  

## Project Structure

```text
.
├── question_1.py            # Solution for Question 1
├── raw_text.txt             # Input file for Q1
├── encrypted_text.txt       # Encrypted output (Q1)
├── decrypted_text.txt       # Decrypted output (Q1)

├── evaluator.py             # Solution for Question 2
├── sample_input.txt         # Input file for Q2
├── output.txt               # Output file for Q2

├── README.md

## Question 1: Encryption & Decryption

### Description
Reads text from `raw_text.txt`, encrypts it, and then decrypts it back to the original text.

### Input
- raw_text.txt

### Output
- encrypted_text.txt  
- decrypted_text.txt  

### Features
- Uses two shift values  
- Handles uppercase and lowercase letters differently  
- Keeps spaces, numbers, and symbols unchanged  
- Verifies decrypted output  

---

## Question 2: Expression Evaluator

### Description
Reads mathematical expressions from a file, evaluates them using recursive descent parsing, and writes the results to an output file.

### File
- evaluator.py

### Input
- sample_input.txt

### Output
- output.txt

### Features
- Supports operators: +, -, *, /  
- Handles nested parentheses  
- Supports unary negation (e.g., -5, -(3+4))  
- Supports implicit multiplication (e.g., 2(3+4))  
- Unary + is not allowed  
- Handles errors (invalid input, division by zero)  
