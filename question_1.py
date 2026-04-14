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


def decrypt_text(text, shift1, shift2):
    result = ""

    for ch in text:
        if ch.islower():
            # lower so negative sifts mulitiplication
            shift = -(shift1 * shift2)
            s = (ord(ch) - ord('a') + shift)
            result += chr( s % 26 + ord('a'))

        elif ch.isupper():
            # upper so negative square - shift
            shift = -(shift2 ** 2 - shift1)
            s = (ord(ch) - ord('A') + shift)
            result += chr( s % 26 + ord('A'))

        else:
            result += ch

    return result

def verify(original, decrypted):
    if original == decrypted:
        print("✅ Decryption Successful!")
    else:
        print("❌ Decryption Failed!")


def main():
    shift1 = int(input("Enter shift1: "))
    shift2 = int(input("Enter shift2: "))

    with open("raw_text.txt", "r") as f:
        raw_text = f.read()

    encrypted = encrypt_text(raw_text, shift1, shift2)
    with open("encrypted_text.txt", "w") as f:
        f.write(encrypted)

    decrypted = decrypt_text(encrypted, shift1, shift2)
    with open("decrypted_text.txt", "w") as f:
        f.write(decrypted)

    verify(raw_text, decrypted)


main()