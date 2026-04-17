def encrypt_text(text, shift1, shift2):
    result = ""

    for ch in text:
        if ch.islower():
            # lower so positive sifts mulitiplication
            shift = shift1 * shift2
            s = (ord(ch) - ord('a') + shift)
            result += chr( s % 26 + ord('a')) # coverting back to ascii text 

        elif ch.isupper():
            # upper so positive square - shift
            shift = shift2 ** 2 - shift1
            s = (ord(ch) - ord('A') + shift)
            result += chr( s % 26 + ord('A'))

        else:
            result += ch

    return result

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

    with open("encrypted_text.txt", "w", encoding="utf-8") as f:
        f.write(encrypted)
    decrypted = decrypt(encrypted, rules, shift1, shift2)

    with open("decrypted_text.txt", "w", encoding="utf-8") as f:
        f.write(decrypted)

    if raw == decrypted:
        print("Decryption Successful")
    else:
        print("Decryption Failed")
main()
