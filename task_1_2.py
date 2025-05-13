from task_1_1 import decrypt_vigenere

def calculate_coincidence_index(ciphertext):
    # Remove non-alphabetic characters and convert to uppercase
    filtered_text = [ch.upper() for ch in ciphertext if ch.isalpha()]
    total_letters = len(filtered_text)
    if total_letters < 2:
        return 0.0

    # Count the frequency of each letter
    frequencies = {}
    for ch in filtered_text:
        frequencies[ch] = frequencies.get(ch, 0) + 1

    # Apply the coincidence index formula
    numerator = sum(freq * (freq - 1) for freq in frequencies.values())
    denominator = total_letters * (total_letters - 1)
    return numerator / denominator if denominator else 0.0


def difference_from_english_frequency(text):
    # Compare frequency distribution of text to expected English letter frequencies
    english_freq = {
        'A': 0.08167, 'B': 0.01492, 'C': 0.02782, 'D': 0.04253, 'E': 0.12702,
        'F': 0.02228, 'G': 0.02015, 'H': 0.06094, 'I': 0.06966, 'J': 0.00153,
        'K': 0.00772, 'L': 0.04025, 'M': 0.02406, 'N': 0.06749, 'O': 0.07507,
        'P': 0.01929, 'Q': 0.00095, 'R': 0.05987, 'S': 0.06327, 'T': 0.09056,
        'U': 0.02758, 'V': 0.00978, 'W': 0.02360, 'X': 0.00150, 'Y': 0.01974,
        'Z': 0.00074
    }

    if not text:
        return 9999.0

    text_length = len(text)
    freq_count = {ch: 0 for ch in english_freq}
    for ch in text:
        if ch in freq_count:
            freq_count[ch] += 1

    for ch in freq_count:
        freq_count[ch] /= text_length

    total_difference = sum(abs(freq_count[ch] - english_freq[ch]) for ch in english_freq)
    return total_difference


def english_likeness_score(text):
    # Heuristic score: more spaces and vowels indicate English-like text
    vowels = set("AEIOUaeiou")
    space_count = text.count(' ')
    vowel_count = sum(ch in vowels for ch in text)
    return space_count + 0.5 * vowel_count


def friedman_test(ciphertext):
    # Estimate key length using the Friedman test
    index = calculate_coincidence_index(ciphertext)
    if index <= 0 or (index - 0.0385) == 0:
        return 1.0
    estimated_length = 0.0279 / (index - 0.0385) + 1
    return estimated_length


def split_text_into_columns(ciphertext, key_length):
    # Organize cifertext into columns based on key length
    filtered = [ch.upper() for ch in ciphertext if ch.isalpha()]
    columns = [[] for _ in range(key_length)]
    for i, ch in enumerate(filtered):
        columns[i % key_length].append(ch)
    return ["".join(column) for column in columns]


def shift_text(text, shift):
    # Use Caesar shift to text
    result = []
    for ch in text:
        if 'A' <= ch <= 'Z':
            shifted_char = (ord(ch) - ord('A') + shift) % 26 + ord('A')
            result.append(chr(shifted_char))
        else:
            result.append(ch)
    return "".join(result)


def find_most_likely_shift(column):
    # Determine Caesar shift for a column by minimizing distance to English letter frequencies
    best_shift = 0
    lowest_difference = float('inf')

    for shift in range(26):
        shifted_column = shift_text(column, -shift)
        difference = difference_from_english_frequency(shifted_column)
        if difference < lowest_difference:
            lowest_difference = difference
            best_shift = shift

    return best_shift


def try_guess_key(ciphertext, max_key_len=15):
    #   1. Estimate the key length using the Friedman test.
    #   2. Try key lengths around the estimated value.
    #   3. For each candidate key length:
    #      a) Split the ciphertext into columns based on key length.
    #      b) Determine the most likely Caesar shift for each column.
    #      c) Build the candidate key.
    #      d) Decrypt the text with this key and score how "English-like" it is.
    #   4. Return the key that gives the best score.
    approx_length = int(round(friedman_test(ciphertext)))
    length_range = range(max(1, approx_length - 2), min(max_key_len, approx_length + 3))

    best_key = ""
    best_score = float('-inf')

    for key_len_candidate in length_range:
        columns = split_text_into_columns(ciphertext, key_len_candidate)
        shifts = [find_most_likely_shift(col) for col in columns]
        candidate_key = "".join(chr(shift + ord('A')) for shift in shifts)

        decrypted_text = decrypt_vigenere(ciphertext, candidate_key)
        score = english_likeness_score(decrypted_text)

        if score > best_score:
            best_score = score
            best_key = candidate_key

    return best_key


if __name__ == "__main__":
    with open('encrypted_text_1_1.txt', "r") as file:
        encrypted_text = file.read()
    estimated_key_length = friedman_test(encrypted_text)
    print(f"Estimated key length: {estimated_key_length:.2f}")

    key_guess = try_guess_key(encrypted_text, max_key_len=15)
    print(f"Guessed key: {key_guess}")

    decrypted_text = decrypt_vigenere(encrypted_text, key_guess)
    print("Decrypted:", decrypted_text)

    with open('text.txt', "r") as file:
        plaintext = file.read()

    if plaintext == decrypted_text:
        print("Texts are the same")
    else:
        print("Texts are different")
