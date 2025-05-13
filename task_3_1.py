def generate_cipher_table(key):
    key = key.upper().replace(" ", "")
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    table = []
    key_set = set()
    for char in key: #fill key
        if char not in key_set and char in alphabet:
            table.append(char)
            key_set.add(char)
    for char in alphabet: #fill with all other letters
        if char not in key_set:
            table.append(char)
    return table

def encrypt(text, key):
    table = generate_cipher_table(key)
    text = text.upper().replace(" ", "")
    encrypted_text = ""
    for char in text:
        if char in table:
            encrypted_text += table[(table.index(char) + 1) % len(table)]
        else:
            encrypted_text += char
    return encrypted_text

def decrypt(text, key):
    table = generate_cipher_table(key)
    text = text.upper().replace(" ", "")
    decrypted_text = ""
    for char in text:
        if char in table:
            decrypted_text += table[(table.index(char) - 1) % len(table)]
        else:
            decrypted_text += char
    return decrypted_text

if __name__ == '__main__':
    key = "MATRIX"
    with open('text.txt', "r") as file:
            plaintext = file.read()
    encrypted_text = encrypt(plaintext, key)
    decrypted_text = decrypt(encrypted_text, key)

    with open('encrypted_text_3_1.txt', "w") as file:
        file.write(encrypted_text)

    print(f"Original text: {plaintext}")
    print(f"Encrypted text: {encrypted_text}")
    print(f"Decrypted text: {decrypted_text}")