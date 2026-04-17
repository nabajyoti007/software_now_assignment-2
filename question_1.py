def encrypt(text, shift1, shift2):
    encrypted = ""
    rules = []

    for ch in text:
        if 'a' <= ch <= 'm':
            new = chr((ord(ch)-97 + shift1*shift2) % 26 + 97)
            rules.append("1")
        elif 'n' <= ch <= 'z':
            new = chr((ord(ch)-97 - (shift1+shift2)) % 26 + 97)
            rules.append("2")
        elif 'A' <= ch <= 'M':
            new = chr((ord(ch)-65 - shift1) % 26 + 65)
            rules.append("3")
        elif 'N' <= ch <= 'Z':
            new = chr((ord(ch)-65 + shift2**2) % 26 + 65)
            rules.append("4")
        else:
            new = ch
            rules.append("0")

        encrypted += new

    return encrypted, rules

def decrypt(text, rules, shift1, shift2):
    decrypted = ""

    for i in range(len(text)):
        ch = text[i]
        rule = rules[i]

        if rule == "1":
            new = chr((ord(ch)-97 - shift1*shift2) % 26 + 97)
        elif rule == "2":
            new = chr((ord(ch)-97 + (shift1+shift2)) % 26 + 97)
        elif rule == "3":
            new = chr((ord(ch)-65 + shift1) % 26 + 65)
        elif rule == "4":
            new = chr((ord(ch)-65 - shift2**2) % 26 + 65)
        else:
            new = ch

        decrypted += new

    return decrypted
def main():
    shift1 = int(input("Enter shift1: "))
    shift2 = int(input("Enter shift2: "))

    with open("raw_text.txt", "r", encoding="utf-8") as f:
        raw = f.read()
    encrypted, rules = encrypt(raw, shift1, shift2)

    with open("Q1 encrypted_text.txt", "w", encoding="utf-8") as f:
        f.write(encrypted)
    decrypted = decrypt(encrypted, rules, shift1, shift2)

    with open("Q1 decrypted_text.txt", "w", encoding="utf-8") as f:
        f.write(decrypted)

    if raw == decrypted:
        print("Decryption Successful")
    else:
        print("Decryption Failed")
main()
