def get_order(key):
    #Return the order of columns based on alphabetical order of the key.
    sorted_key = sorted(list(enumerate(key)), key=lambda x: (x[1], x[0]))
    order = [index for index, _ in sorted_key]
    return order

def encrypt(text, key):
    key_len = len(key)
    col_order = get_order(key)

    padded_len = ((len(text) + key_len - 1) // key_len) * key_len
    padded_text = text.ljust(padded_len, 'X') # add Xes in the end of text to match key length in all rows (it will be bed situation if text ends with 'x')

    # Break text into rows
    rows = []
    for i in range(0, len(padded_text), key_len): #create rows
        row = padded_text[i:i + key_len]
        rows.append(row)

    # Read columns in the new order
    ciphertext = ''
    for col_index in col_order:
        for row in rows:
            ciphertext += row[col_index]
    return ciphertext

def decrypt(ciphertext, key):
    key_len = len(key)
    col_order = get_order(key)
    num_rows = len(ciphertext) // key_len

    # Divide into columns
    columns = []
    for i in range(key_len):
        columns.append(ciphertext[i * num_rows:(i + 1) * num_rows])

    # Place columns back in original order
    reordered_columns = [''] * key_len
    for i, col_index in enumerate(col_order):
        reordered_columns[col_index] = columns[i]

    # Rebuild text row by row
    plaintext = ''
    for i in range(num_rows):
        for col in reordered_columns:
            plaintext += col[i]
    return plaintext.rstrip('X') #revove xes in end


if __name__ == '__main__':
    key = "SECRET"
    with open('text.txt', "r") as file:
        plaintext = file.read()

    chipertext = encrypt(plaintext, key)
    with open('encrypted_text_2_1.txt', "w") as file:
        file.write(chipertext)
    
    print(f"Encrypted text: {chipertext}")

    decrypted_text = decrypt(chipertext, key)
    print(f"Decrypted text: {decrypted_text}")

    if(plaintext == decrypted_text):
        print("Texts are the same")
    else:
        print("Texts are different")