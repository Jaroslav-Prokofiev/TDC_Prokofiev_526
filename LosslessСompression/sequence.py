import random
import string
import collections
import math
import matplotlib.pyplot as plt

N_sequence = 100
open("results_sequence.txt", "w").close()

#Послідовність №1
N1 = 5
list1 = []
for i in range(N1):
    list1.append('1')

list0 = []
for i in range(N_sequence - N1):
    list0.append('0')

sequence_list = list1 + list0

random.shuffle(sequence_list)

original_sequence_1 = ""
for symbol in sequence_list:
    original_sequence_1 = original_sequence_1 + symbol

unique_chars = set(original_sequence_1)
alphabet_size = len(unique_chars)

size_bytes = len(original_sequence_1)
size_bits = size_bytes * 8

file = open("results_sequence.txt", "a", encoding="utf-8")
file.write("Послідовність №1\n")
file.write("Послідовність: " + original_sequence_1 + "\n")
file.write("Розмір алфавіту: " + str(alphabet_size) + "\n")
file.write("Розмір: " + str(size_bytes) + " байт\n")
file.write("Розмір: " + str(size_bits) + " біт\n")
file.write("\n")

'''print("Послідовність №1:")
print(original_sequence_1)
print("Алфавіт:", alphabet_size)
print("Розмір:", size_bytes, "байт")'''

lastname = 'Prokofiev'

list1 = [] #Послідовність №2
for letter in lastname:
    list1.append(letter)

N1 = len(list1)
N0 = N_sequence - N1

list0 = []
for i in range(N0):
    list0.append('0')

sequence_list = list1 + list0

original_sequence_2 = ""
for symbol in sequence_list:
    original_sequence_2 += symbol

alphabet_size_2 = len(set(original_sequence_2))

size_bytes_2 = len(original_sequence_2)
size_bits_2 = size_bytes_2 * 8

file = open("results_sequence.txt", "a", encoding="utf-8")
file.write("Послідовність №2\n")
file.write("Послідовність: " + original_sequence_2 + "\n")
file.write("Розмір алфавіту: " + str(alphabet_size_2) + "\n")
file.write("Розмір: " + str(size_bytes_2) + " байт\n")
file.write("Розмір: " + str(size_bits_2) + " біт\n\n")

list1 = [] #Послідовність №3
for letter in lastname:
    list1.append(letter)

N1 = len(list1)
N0 = N_sequence - N1

list0 = []
for i in range(N0):
    list0.append('0')

sequence_list_3 = list1 + list0
random.shuffle(sequence_list_3)

original_sequence_3 = ""
for symbol in sequence_list_3:
    original_sequence_3 += symbol

alphabet_size_3 = len(set(original_sequence_3))

size_bytes_3 = len(original_sequence_3)
size_bits_3 = size_bytes_3 * 8

file = open("results_sequence.txt", "a", encoding="utf-8")
file.write("Послідовність №3\n")
file.write("Послідовність: " + original_sequence_3 + "\n")
file.write("Розмір алфавіту: " + str(alphabet_size_3) + "\n")
file.write("Розмір: " + str(size_bytes_3) + " байт\n")
file.write("Розмір: " + str(size_bits_3) + " біт\n\n")

group = "526"

letters = [] #Послідовність №4

for ch in lastname:
    letters.append(ch)

for ch in group:
    letters.append(ch)

n_letters = len(letters)
n_repeats = N_sequence // n_letters
remainder = N_sequence % n_letters
sequence_list = letters * n_repeats
sequence_list += letters[:remainder]
original_sequence_4 = ''.join(map(str, sequence_list))
alphabet_size_4 = len(set(original_sequence_4))
size_bytes_4 = len(original_sequence_4)
size_bits_4 = size_bytes_4 * 8

file = open("results_sequence.txt", "a", encoding="utf-8")
file.write("Послідовність №4\n")
file.write("Послідовність: " + original_sequence_4 + "\n")
file.write("Розмір алфавіту: " + str(alphabet_size_4) + "\n")
file.write("Розмір: " + str(size_bytes_4) + " байт\n")
file.write("Розмір: " + str(size_bits_4) + " біт\n\n")

letters = [] #Послідовність №5
letters.append(lastname[0])
letters.append(lastname[1])

for ch in group:
    letters.append(ch)
    
sequence_list = []

for i in range(N_sequence):

    symbol = random.choice(letters)
    sequence_list.append(symbol)

random.shuffle(sequence_list)

original_sequence_5 = ""
for ch in sequence_list:
    original_sequence_5 += ch

alphabet_size_5 = len(set(original_sequence_5))

size_bytes_5 = len(original_sequence_5)
size_bits_5 = size_bytes_5 * 8

file = open("results_sequence.txt", "a", encoding="utf-8")
file.write("Послідовність №5\n")
file.write("Послідовність: " + original_sequence_5 + "\n")
file.write("Розмір алфавіту: " + str(alphabet_size_5) + "\n")
file.write("Розмір: " + str(size_bytes_5) + " байт\n")
file.write("Розмір: " + str(size_bits_5) + " біт\n\n")


letters = [] #Послідовність №6
letters.append(lastname[0])
letters.append(lastname[1])

digits = []
for ch in group:
    digits.append(ch)

n_letters = int(0.7 * N_sequence)
n_digits = int(0.3 * N_sequence)

list_100 = []

for i in range(n_letters):
    list_100.append(random.choice(letters))

for i in range(n_digits):
    list_100.append(random.choice(digits))

random.shuffle(list_100)

original_sequence_6 = ""
for ch in list_100:
    original_sequence_6 += ch

alphabet_size_6 = len(set(original_sequence_6))
size_bytes_6 = len(original_sequence_6)
size_bits_6 = size_bytes_6 * 8

file = open("results_sequence.txt", "a", encoding="utf-8")
file.write("Послідовність №6\n")
file.write("Послідовність: " + original_sequence_6 + "\n")
file.write("Розмір алфавіту: " + str(alphabet_size_6) + "\n")
file.write("Розмір: " + str(size_bytes_6) + " байт\n")
file.write("Розмір: " + str(size_bits_6) + " біт\n\n")

elements = string.ascii_lowercase + string.digits #Послідовність №7
list_100 = [random.choice(elements) for _ in range(N_sequence)]
original_sequence_7 = ''.join(list_100)
alphabet_size_7 = len(set(original_sequence_7))

size_bytes_7 = len(original_sequence_7)
size_bits_7 = size_bytes_7 * 8

file = open("results_sequence.txt", "a", encoding="utf-8")
file.write("Послідовність №7\n")
file.write("Послідовність: " + original_sequence_7 + "\n")
file.write("Розмір алфавіту: " + str(alphabet_size_7) + "\n")
file.write("Розмір: " + str(size_bytes_7) + " байт\n")
file.write("Розмір: " + str(size_bits_7) + " біт\n\n")

original_sequence_8 = '1' * N_sequence #Послідовність №8
alphabet_size_8 = len(set(original_sequence_8))

size_bytes_8 = len(original_sequence_8)
size_bits_8 = size_bytes_8 * 8

file = open("results_sequence.txt", "a", encoding="utf-8")
file.write("Послідовність №8\n")
file.write("Послідовність: " + original_sequence_8 + "\n")
file.write("Розмір алфавіту: " + str(alphabet_size_8) + "\n")
file.write("Розмір: " + str(size_bytes_8) + " байт\n")
file.write("Розмір: " + str(size_bits_8) + " біт\n\n")

results = []

original_sequences = [original_sequence_1, original_sequence_2, original_sequence_3, original_sequence_4, original_sequence_5, original_sequence_6, original_sequence_7, original_sequence_8]
with open("sequence.txt", "w", encoding="utf-8") as f:
    for i, seq in enumerate(original_sequences, start=1):
        f.write("Послідовність №" + str(i) + "\n")
        f.write(seq + "\n\n")

with open("results_sequence.txt", "a", encoding="utf-8") as file:

    for i, sequence in enumerate(original_sequences, start=1):
        counts = collections.Counter(sequence)
        probability = {symbol: count / N_sequence for symbol, count in counts.items()}
        mean_probability = sum(probability.values()) / len(probability)
        equal = all(abs(prob - mean_probability) < 0.05 * mean_probability for prob in probability.values())

        if equal:
            uniformity = "рівна"
        else:
            uniformity = "нерівна"

        entropy = -sum(p * math.log2(p) for p in probability.values())
        sequence_alphabet_size = len(counts)

        if sequence_alphabet_size > 1:
            source_excess = 1 - entropy / math.log2(sequence_alphabet_size)
        else:
            source_excess = 1

        probability_str = ', '.join([f"{symbol}={prob:.4f}" for symbol, prob in probability.items()])
        results.append([sequence_alphabet_size, round(entropy, 2), round(source_excess, 2), uniformity])
        file.write("Послідовність №" + str(i) + "\n")
        file.write("Ймовірності: " + probability_str + "\n")
        file.write("Середня ймовірність: " + str(round(mean_probability, 4)) + "\n")
        file.write("Тип розподілу: " + uniformity + "\n")
        file.write("Ентропія: " + str(round(entropy, 4)) + "\n")
        file.write("Надмірність: " + str(round(source_excess, 4)) + "\n\n")

fig, ax = plt.subplots(figsize=(14/1.54, 8/1.54))
headers = ['Розмір алфавіту', 'Ентропія', 'Надмірність', 'Ймовірність']
row = ['Послідовність 1', 'Послідовність 2', 'Послідовність 3', 'Послідовність 4', 'Послідовність 5', 'Послідовність 6','Послідовність 7', 'Послідовність 8']
ax.axis('off')
table = ax.table(cellText=results, colLabels=headers, rowLabels=row, loc='center', cellLoc='center')
table.set_fontsize(14)
table.scale(0.8, 2)
fig.savefig("Характеристики.png")
plt.show()