"""
Given a file containing text. Complete using only default collections:
    1) Find 10 longest words consisting from largest amount of unique symbols
    2) Find rarest symbol for document
    3) Count every punctuation char
    4) Count every non ascii char
    5) Find most common non ascii char for document
"""
from typing import List
from collections import Counter

def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
    return content.encode('utf-8').decode('unicode-escape')

text = read_file("data.txt")

word_list = text.split()  # Разделяем текст на слова

def get_longest_diverse_words(file_path: str,top_n=10) -> List[str]:
    words = text.split()
    sorted_words = sorted(words, key=lambda x: (-len(x), -len(set(x))))
    print("10 longest words with most unique symbols:", sorted_words[:top_n])

def get_rarest_char(file_path: str) -> str:
    rarest_c = Counter(text)
    print("rarest symbol: " + str(rarest_c.most_common()[-1][0]))


def count_punctuation_chars(file_path: str) -> int:
    punct = 0
    for char in text:
        if char in [',','.','!',':',';','"','','?']:
            punct += 1
    print("punctuation chars: "+str(punct))


def count_non_ascii_chars(file_path: str) -> int:
    non_ascii_count = 0
    for char in text:
        if not char.isascii():
            non_ascii_count += 1
    print("non ascii chars: "+ str(non_ascii_count))


def get_most_common_non_ascii_char(file_path: str) -> str:
    non_ascii_chars = [char for char in text if not char.isascii()]
    if not non_ascii_chars:
        return None
    counter = Counter(non_ascii_chars)
    return counter.most_common(1)[0]

longest_words = get_longest_diverse_words(text)

count_non_ascii_chars(text)

count_punctuation_chars(text)

get_rarest_char(text)

most_common_non_ascii = get_most_common_non_ascii_char(text)
print("Most common non-ASCII char:", most_common_non_ascii)
