from typing import List
import json

polish_alphabet = ['a', 'ą', 'b', 'c', 'ć', 'd', 'e', 'ę', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'ł', 'm', 'n', 'ń', 'o', 'ó', 'p', 'q', 'r', 's', 'ś', 't', 'u', 'w', 'x', 'y', 'z', 'ź', 'ż']

def read_txt_file(path: str, n_elements: int = 0) -> str:
    '''
    This function receives path to .txt file that later returns as list of words.
    '''
    with open(path, "r", encoding="utf8") as file:  # open file

        lines = file.readlines()  # file's lines

        # Format and filter all words
        all_words = [] # all words are stored here
        for line in lines:
            if line != '\n':
                # split to words
                words = line.split(' ')
                for word in words:
                    if word not in ['—', '—', '', ' ', 'ISBN', '978-83-288-2495-9\n']:  # if return str, delete ' '
                        complete_word = ''
                        for letter in word:
                            if letter.lower() in polish_alphabet:
                                complete_word += letter
                        all_words.append(complete_word)
        # Return n words
        if n_elements != 0:
            data_to_return = []
            for word_index in range(0, n_elements):
                data_to_return.append(all_words[word_index])
            return data_to_return  # list_2_str(data_to_return)
        else:
            return all_words  # list_2_str(all_words)

def list_2_str(data: List[str]) -> str:
    '''Converts list with str to str'''
    str_return = ''
    for element in data:
        str_return += f'{element} '
    return str_return

def print_results(dict_of_words: dict[str, List[int]], text: str) -> None:
    '''This function gets indecies in which the substring has appeared.
    It prints out results in the original test with a margin of 2 letters'''
    for word in dict_of_words.keys():
        print(f'Word: {word}')
        word_length = len(word)
        for index in dict_of_words[word]:
            start = index-2
            end = index+word_length+2
            if start<0:
                start=0
            print(f'Indeks: {index} Słowa: {text[start:end]}')

'''
GET DATA FROM BENCHMARK FILES
'''

def search_for_data(path):
    data = read_json_file(path)
    benchmarks = data['benchmarks']

    min_time = []  # list that holds minimum time of performing algorithm
    data_length = []  # list that holds number of data used in benchmark

    for benchmarks in benchmarks:
        stats = benchmarks['stats']
        min_time.append(stats['min'])
        data_length.append(get_length(benchmarks['name']))
    return min_time, data_length

def read_json_file(path: str) -> List:
    '''
    This function receives path to .json file that later returns list.
    '''
    with open(path, "r") as filehandle:  # open file
        data = json.load(filehandle)
        return data

def get_length(name: str) -> int:
    '''Returns number from the name'''
    length = ''
    for character in name:  # iterate through every character
        if character.isdigit():
            length += character
    return int(length)