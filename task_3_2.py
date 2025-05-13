from task_1_1 import encrypt_vigenere, decrypt_vigenere
from task_3_1 import encrypt, decrypt

if __name__ == '__main__':
    key = "CRYPTO"
    with open('text.txt', "r") as file:
            plaintext = file.read()
    encrypted_text = encrypt_vigenere(plaintext, key)
    encrypted_text1 = encrypt(encrypted_text,key)
    decrypted_text1 = decrypt(encrypted_text1,key)
    decrypted_text = decrypt_vigenere(decrypted_text1, key)


    print(f"Encrypted text: {encrypted_text}\n")
    print(f"Encrypted text1: {encrypted_text1}\n")
    print(f"Decrypted text1: {decrypted_text1}\n")
    print(f"Decrypted text: {decrypted_text}")


    with open('encrypted_text_3_2.txt', "w") as file:
        file.write(encrypted_text1)
