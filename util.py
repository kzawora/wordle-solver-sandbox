from audioop import mul
from corpus import validwords_corpus
from collections import Counter
from functools import wraps
from math import prod 

def get_letter_counts(corpus):
    return Counter(list(''.join(corpus)))
        
def get_letter_probability(corpus):
    counter = get_letter_counts(corpus)
    total = sum(counter.values())
    result = {key:value/total for key, value in counter.items()}
    return result
    
def get_letter_probability_score_for_word(word, letter_probability):
    return sum([letter_probability[letter] for letter in set(word)])

if __name__ == '__main__':
    print(get_letter_counts(validwords_corpus))
    print(get_letter_probability(validwords_corpus))