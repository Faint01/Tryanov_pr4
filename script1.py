import multiprocessing
from multiprocessing import Process
from random import randint
from typing import List
from RandomWordGenerator import RandomWord
import os

def name_file(name_file):
    file = open(name_file, 'r')
    l = 0
    for line in file:
        l += 1
    file.close()
    return l

def total(name_file: str):
    file = open(name_file, 'r')
    t = 0
    for line in file:
        for ch in line:
            if ch != '\n':
                t += len(ch)
    file.close()
    return t

def max_length(name_file: str):
    file = open(name_file, 'r')
    maxlen: int = -1
    for line in file:
        line = line.replace("\n", "")
        if line != '':
            if maxlen == -1:
                maxlen = len(line)
            else:
                if maxlen < len(line):
                    maxlen = len(line)
    file.close()
    return maxlen

def min_length(name_file: str):
    file = open(name_file, 'r')
    minlen: int = -1
    for line in file:
        line = line.replace("\n", "")
        if line != '':
            if minlen == -1:
                minlen = len(line)
            else:
                if minlen > len(line):
                    minlen = len(line)
    file.close()
    return minlen

def mid_length(name_file: str):
    midlen: float = total(name_file) / name_file(name_file)
    return midlen

def vowel(name_file: str):
    file = open(name_file, 'r')
    vow: int = 0
    for line in file:
        for ch in line:
            if ch in ['a', 'e', 'i', 'o', 'u', 'y', 'A', 'E', 'I', 'O', 'U', 'Y']:
                vow += 1
            else:
                pass
    file.close()
    return vow

def consonant(name_file: str):
    file = open(name_file, 'r')
    consonant: int = 0
    for line in file:
        for ch in line:
            if ch in ['a', 'e', 'i', 'o', 'u', 'y', 'A', 'E', 'I', 'O', 'U', 'Y', '\n', ' ']:
                pass
            else:
                consonant += 1
    file.close()
    return consonant

def repetitions(name_file: str):
    file = open(name_file, 'r')
    rep_dict: dict = dict()

    for line in file:
        line = line.replace("\n", "")
        if line != '':
            if len(line) in rep_dict:
                rep_dict[len(line)] += 1
            else:
                rep_dict[len(line)] = 1

    sorted_dict = {}
    sorted_keys = sorted(rep_dict.keys())

    for w in sorted_keys:
        sorted_dict[w] = rep_dict[w]
    rep_dict = sorted_dict.copy()

    rep: str = ""
    for key in rep_dict:
        rep += f"   * {key} сим. >> {rep_dict[key]} повторений.\n"
    file.close()
    return rep

def analytics(name_file: str):

    t:str = ""
    for i in range(55):
        t += '*'

    print(t + f"\n" + f"Аналитика для файла {name_file}" + f"\n" + t + f"\n" +
          f"1. Всего символов --> {total(name_file)}\n" +
          f"2. Максимальная длина слова --> {max_length(name_file)}\n" +
          f"3. Минимальная длина слова --> {min_length(name_file)}\n" +
          f"4. Средняя длина слова --> {mid_length(name_file)}\n" +
          f"5. Количество гласных --> {vowel(name_file)}\n" +
          f"6. Количество согласных --> {consonant(name_file)}\n" +
          "7. Количество повторений слов с одинаковой длиной:\n"+
          f"{repetitions(name_file)} \n")

def create_files(num: int, quantity: int):
    random_word = RandomWord()
    random_word.constant_word_size = False
    pid: int = os.getpid()
    name_file: str = f'./result_files/Process-{num}-{pid}.txt'
    file = open(name_file, 'a')
    for q in range(quantity):
        file.write(f'{random_word.generate()}\n')
    file.close()
    analytics(name_file)

if __name__ == '__main__':
    manager = multiprocessing.Manager()

    list_process: List[Process] = []

    for i in range(multiprocessing.cpu_count()):
        name_pr: str = f"pr{i}"
        quant: int = randint(1, 11)
        pr: Process = Process(target=create_files, args = (i+1, quant), name=name_pr)
        list_process.append(pr)
        pr.start()

    for i in range(multiprocessing.cpu_count()):
        list_process[i].join()