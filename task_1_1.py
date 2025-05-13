def vigenere_cipher(text, key, mode):
    key = key.upper() #set all upper to easy shift calculation
    key_length = len(key)
    key_index = 0
    result = ''

    for char in text:
        if char.isalpha():
            key_char = key[key_index % key_length] #get key letter in cycle to extend key for text lenght
            key_shift = ord(key_char) - ord('A') #calculate shift
            if char.isupper():
                start = ord('A')
            else:
                start = ord('a')

            if mode == 'encrypt':
                shifted_char = chr((ord(char) - start + key_shift) % 26 + start) #search shifted char
            elif mode == 'decrypt':
                shifted_char = chr((ord(char) - start - key_shift) % 26 + start)
            else:
                raise ValueError("Use 'encrypt' or 'decrypt'")

            result += shifted_char
            key_index += 1
        else: #if not char
            result += char

    return result


def encrypt_vigenere(text, key):
    return vigenere_cipher(text, key, 'encrypt')


def decrypt_vigenere(ciphertext, key):
    return vigenere_cipher(ciphertext, key, 'decrypt')


if __name__ == '__main__':
    key = "CRYPTOGRAPHY"

    with open('text.txt', "r") as file:
        plaintext = file.read()
    
    
    ciphertext = encrypt_vigenere(plaintext, key)
    with open('encrypted_text_1_1.txt', "w") as file:
        file.write(ciphertext)

    decrypted_text = decrypt_vigenere(ciphertext, key)
    if plaintext == decrypted_text:
        print("Texts are the same")
    else:
        print("Texts are different")
    