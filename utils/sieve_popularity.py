import json
from typing import DefaultDict
import morfeusz2
import re
from collections import defaultdict
import random

morf = morfeusz2.Morfeusz()

tags_to_delete = set(
    [
        "burk",
        "conj",
        "comp",
        "num",
        "ppron12",
        "ppron3",
        "pred",
        "prep",
        "siebie",
        "brev",
        "qub",
        "wulg",
        "interj",
    ]
)


def sieve_popularity_dict(popularity_file):
    with open(popularity_file, "r", encoding="utf-8") as popularity:
        dicti = json.load(popularity)
        words_to_del = set()
        for word in dicti:
            word_tags_set = set()
            for tup in morf.analyse(word):
                further_analysis = (tup[2])[2].split(":")
                for e in further_analysis:
                    word_tags_set.add(e)
            if len(word_tags_set) == 1:
                words_to_del.add(word)
            if len(word_tags_set.intersection(tags_to_delete)) != 0:
                words_to_del.add(word)
        for word in words_to_del:
            del dicti[word]
        with open("sieved_popularity.json", "w", encoding="utf-8") as save:
            json.dump(dicti, save, ensure_ascii=False)


# sieve_popularity_dict("popularity.json")


def reverse_popularity_dict(popularity_file):
    with open(popularity_file, "r", encoding="utf-8") as popularity:
        dicti = json.load(popularity)
        desc_ord = dict(sorted(dicti.items(), key=lambda item: item[1], reverse=True))
        with open("reverse_pop.json", "w", encoding="utf-8") as save:
            json.dump(desc_ord, save, ensure_ascii=False)


# reverse_popularity_dict("popularity.json")


def cut_to_n_keys(popularity_file, n):
    with open(popularity_file, "r", encoding="utf-8") as popularity:
        dicti = json.load(popularity)
        n_items = {k: dicti[k] for k in list(dicti.keys())[:n]}
        with open(str(n) + "_popularity_items.json", "w", encoding="utf-8") as save:
            json.dump(n_items, save, ensure_ascii=False)


# cut_to_n_keys("reverse_pop.json", 100000)


def sieve_corpus_to_leave_populars(corpus, pop_dict):
    with open(corpus, "r", encoding="utf-8") as corp:
        with open(pop_dict, "r", encoding="utf-8") as popul:
            with open("corpus_with_populars.txt", "w", encoding="utf-8") as f:
                pop_dic = json.load(popul)
                keys_set = set(pop_dic.keys())
                for line in corp:
                    line = line.rstrip()
                    guard = 1
                    for word in tokenize(line):
                        word = word.strip()
                        if word not in keys_set:
                            guard = 0
                            continue
                    if guard == 1:
                        f.write(line + "\n")


# sieve_corpus_to_leave_populars("pl_tok_sieved.txt", "100000_popularity_items.json")


def tokenize(line):
    text = line.lower()
    pattern = r"\s*\w*\s*"
    return list(filter(None, re.findall(pattern, text)))


def create_indexes_dict():
    with open("corpus_with_populars.txt", "r", encoding="utf-8") as corp:
        with open("sieved_popularity.json", "r", encoding="utf-8") as pops:
            pops_dict = json.load(pops)
            keys_set = set(pops_dict.keys())
            indexes = defaultdict(list)
            for index, line in enumerate(corp):
                line = line.strip()
                for word in tokenize(line):
                    word = word.strip()
                    if word in keys_set:
                        indexes[word].append(index)

            for word in indexes:
                val = indexes[word]
                random.shuffle(val)
                indexes[word] = val[:1000]
    with open("index_dict.json", "w", encoding="utf-8") as save:
        json.dump(indexes, save, ensure_ascii=False)


# create_indexes_dict()


def see_indexes():
    with open("index_dict.json", "r", encoding="utf-8") as save:
        index_dict = json.load(save)
        i = 0
        for j, indexes in index_dict.items():
            print(j, indexes)
            print()
            i += 1
            if i > 5:
                break


see_indexes()


# def cut_indexes_lists():
#     with open("index_dict.json", "r", encoding="utf-8") as dicti:
#         index_dict = json.load(dicti)
#         for key in index_dict:
#             if len(index_dict[key]) > 1000:
#                 val = index_dict[key]
#                 random.shuffle(val)
#                 index_dict[key] = val[:1000]
#     with open("indexes_narrowed.json", "w", encoding="utf-8") as save:
#         json.dump(index_dict, save, ensure_ascii=False)


# cut_indexes_lists()
