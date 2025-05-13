from task_2_1 import get_order, encrypt, decrypt


def encrypt_row_transposition(text, key):
    key_len = len(key)
    row_order = get_order(key)
    num_cols = (len(text) + key_len - 1) // key_len
    padded_text = text.ljust(num_cols * key_len, 'X')

    #create init rows
    rows = [padded_text[i * num_cols:(i + 1) * num_cols] for i in range(key_len)]

    # rearrange rows
    reordered_rows = [rows[i] for i in row_order]

    # read by columns
    ciphertext = ''.join(reordered_rows[row][col] for col in range(num_cols) for row in range(key_len))
    return ciphertext


def decrypt_row_transposition(ciphertext, key):
    key_len = len(key)
    row_order = get_order(key)
    num_cols = len(ciphertext) // key_len

    # create table
    matrix = [['' for _ in range(num_cols)] for _ in range(key_len)]
    index = 0
    for col in range(num_cols):
        for row in range(key_len):
            matrix[row][col] = ciphertext[index]
            index += 1

    # rearange rows back
    original_matrix = [''] * key_len
    for i, row_index in enumerate(row_order):
        original_matrix[row_index] = ''.join(matrix[i])

    return ''.join(original_matrix)#.rstrip('X') #cant remove last xes if double ciphering


if __name__ == '__main__':
    key = "SECRET"
    key1 = "CRYPTO"
    with open('text.txt', "r") as file:
        plaintext = file.read()

   # plaintext = "this is a test"

    ciphertext = encrypt(plaintext, key)
    print(f"Encrypted text 1: {ciphertext}")

    ciphertext1 = encrypt_row_transposition(ciphertext, key1)
    print(f"Encrypted text 2: {ciphertext1}")
    with open('encrypted_text_2_2.txt', "w") as file:
        file.write(ciphertext1)


    decrypted_text = decrypt_row_transposition(ciphertext1, key1)
    print(f"Decrypted text: {decrypted_text}")

    decrypted_text = decrypt(decrypted_text, key)
    print(f"Decrypted text: {decrypted_text}")

    if plaintext == decrypted_text:
        print("Texts are the same")
    else:
        print("Texts are different")
