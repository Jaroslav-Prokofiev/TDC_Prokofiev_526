import collections
import math
import matplotlib.pyplot as plt
import ast

N_sequence = 100
BITS_PER_SYMBOL = 16

with open("sequence.txt", "r") as file:
    original_sequences = ast.literal_eval(file.read())
    original_sequences = [sequence.strip("[]").strip("'").strip('"') for sequence in original_sequences]

with open("results_rle_lzw.txt", "w", encoding="utf-8") as result_file:

    for i, sequence in enumerate(original_sequences, start=1):

        counts = collections.Counter(sequence)
        probability = {symbol: count / N_sequence for symbol, count in counts.items()}
        entropy = -sum(p * math.log2(p) for p in probability.values())
        total_bits = len(sequence) * BITS_PER_SYMBOL

        result_file.write(f"Послідовність №{i}\n")
        result_file.write(f"Послідовність: {sequence}\n")
        result_file.write(f"Кількість появ символів: {dict(counts)}\n")
        result_file.write("Ймовірності символів:\n")

        for symbol, prob in probability.items():
            result_file.write(f"  '{symbol}' : {prob:.4f}\n")

        result_file.write(f"Ентропія: {entropy:.4f} біт/символ\n")
        result_file.write(f"Кількість біт для представлення: {total_bits} біт\n")
        result_file.write("/" * 70 + "\n")


def encode_rle(sequence):
    count = 1
    result = []

    for i, item in enumerate(sequence):
        if i == 0:
            continue
        elif item == sequence[i - 1]:
            count += 1
        else:
            result.append((sequence[i - 1], count))
            count = 1

    result.append((sequence[len(sequence) - 1], count))

    encoded = []
    for i, item in enumerate(result):
        encoded.append(f"{item[1]}{item[0]}")

    return "".join(encoded), result

def decode_rle(sequence):
    result = []

    for item in sequence:
        result.append(item[0] * item[1])

    return "".join(result)

with open("results_rle_lzw.txt", "a", encoding="utf-8") as result_file:
    for i, sequence in enumerate(original_sequences, start=1):
        result_file.write(f"\n")
        result_file.write(f"Оригінальна послідовність: {sequence}\n")
        result_file.write(f"Розмір оригінальної послідовності {len(sequence) * BITS_PER_SYMBOL} bits\n")

        counts = collections.Counter(sequence)
        probability = {symbol: count / N_sequence for symbol, count in counts.items()}
        entropy = -sum(p * math.log2(p) for p in probability.values())
        result_file.write(f"Ентропія: {entropy:.4f}\n")

        result_file.write(f"\n-----Кодування_RLE-----\n")

        encoded_sequence, encoded = encode_rle(sequence)

        if len(encoded_sequence) > 60:
            part1 = encoded_sequence[:60]
            part2 = encoded_sequence[60:]
            result_file.write(f"Закодована RLE послідовність: {part1}\n")
            result_file.write(f"    {part2}\n")
        else:
            result_file.write(f"Закодована RLE послідовність: {encoded_sequence}\n")

        result_file.write(f"Розмір закодованої RLE послідовності: {len(encoded_sequence) * 8} bits\n")

        compression_ratio_RLE = round((len(sequence) / len(encoded_sequence)), 2)
        if compression_ratio_RLE < 1:
            compression_ratio_RLE = '-'

        result_file.write(f"Коефіцієнт стиснення RLE: {compression_ratio_RLE}\n")
        decoded_sequence = decode_rle(encoded)
        result_file.write(f"Декодована RLE послідовність: {decoded_sequence}\n")
        result_file.write(f"Розмір декодованої RLE послідовності: {len(decoded_sequence) * BITS_PER_SYMBOL} bits\n")


def encode_lzw(sequence, result_file):
    dictionary = {}
    for i in range(65536):
        dictionary[chr(i)] = i

    result = []
    current = ""
    total_bits = 0

    for c in sequence:
        new_str = current + c

        if new_str in dictionary:
            current = new_str
        else:
            result.append(dictionary[current])

            if dictionary[current] < 65536:
                element_bits = 16
            else:
                element_bits = math.ceil(math.log2(len(dictionary)))

            total_bits += element_bits
            result_file.write(f"Code: {dictionary[current]}, Element: {current}, Bits: {element_bits}\n")

            dictionary[new_str] = len(dictionary)
            current = c

    if current:
        result.append(dictionary[current])

        if dictionary[current] < 65536:
            last_bits = 16
        else:
            last_bits = math.ceil(math.log2(len(dictionary)))

        total_bits += last_bits
        result_file.write(f"Code: {dictionary[current]}, Element: {current}, Bits: {last_bits}\n")

    return result, total_bits

def decode_lzw(codes):
    dictionary = {}
    for i in range(65536):
        dictionary[i] = chr(i)

    result = ""
    previous = None
    current = ""

    for code in codes:
        if code in dictionary:
            current = dictionary[code]
            result += current
            if previous is not None:
                dictionary[len(dictionary)] = previous + current[0]
            previous = current
        else:
            current = previous + previous[0]
            result += current
            dictionary[len(dictionary)] = current
            previous = current

    return result


with open("results_rle_lzw.txt", "a", encoding="utf-8") as result_file:
    for i, sequence in enumerate(original_sequences, start=1):
        result_file.write(f"\n-----Кодування_LZW-----\n")
        result_file.write(f"-----Словник-----\n")

        lzw_codes, lzw_size = encode_lzw(sequence, result_file)

        result_file.write(f"\nЗакодована LZW послідовність: {''.join(map(str, lzw_codes))}\n")
        result_file.write(f"Розмір закодованої LZW послідовності: {lzw_size} bits\n")

        original_bits = len(sequence) * BITS_PER_SYMBOL
        compression_ratio_LZW = round((original_bits / lzw_size), 2)
        result_file.write(f"Коефіцієнт стиснення LZW: {compression_ratio_LZW}\n")

        decoded_lzw = decode_lzw(lzw_codes)

        result_file.write(f"Декодована LZW послідовність: {decoded_lzw}\n")
        result_file.write(f"Розмір декодованої LZW послідовності: {len(decoded_lzw) * BITS_PER_SYMBOL} bits\n")
        result_file.write("/" * 70 + "\n")

results = []

for i, sequence in enumerate(original_sequences, start=1):
    counts = collections.Counter(sequence)
    probability = {symbol: count / N_sequence for symbol, count in counts.items()}
    entropy = -sum(p * math.log2(p) for p in probability.values())

    encoded_sequence_rle, encoded = encode_rle(sequence)
    compression_ratio_RLE = round((len(sequence) / len(encoded_sequence_rle)), 2)
    if compression_ratio_RLE < 1:
        compression_ratio_RLE = '-'

    dictionary = {}
    for j in range(65536):
        dictionary[chr(j)] = j

    current = ""
    total_bits = 0

    for c in sequence:
        new_str = current + c
        if new_str in dictionary:
            current = new_str
        else:
            if dictionary[current] < 65536:
                total_bits += 16
            else:
                total_bits += math.ceil(math.log2(len(dictionary)))
            dictionary[new_str] = len(dictionary)
            current = c

    if current:
        if dictionary[current] < 65536:
            total_bits += 16
        else:
            total_bits += math.ceil(math.log2(len(dictionary)))

    compression_ratio_LZW = round((len(sequence) * 16 / total_bits), 2)

    results.append([round(entropy, 2    ), compression_ratio_RLE, compression_ratio_LZW])

fig, ax = plt.subplots(figsize=(14/1.54, 8/1.54))
headers = ['Ентропія', 'КС RLE', 'КС LZW']
row = ['Послідовність 1', 'Послідовність 2', 'Послідовність 3', 'Послідовність 4', 'Послідовність 5', 'Послідовність 6', 'Послідовність 7', 'Послідовність 8']
ax.axis('off')
table = ax.table(cellText=results, colLabels=headers, rowLabels=row, loc='center', cellLoc='center')
table.set_fontsize(14)
table.scale(0.8, 2)
fig.savefig("Результати стиснення методами RLE та LZW")
plt.show()