from collections import namedtuple
greensquare = '🟩' 
orangesquare = '🟧'
blanksquare = '⬜'
LetterAndPosition = namedtuple('LetterAndPosition', ['letter', 'position'])

class Game:
    def __init__(self, validwords_corpus, answer, printouts = True):
        self.validwords_corpus = validwords_corpus
        self.answer = answer
        self.guesses = []
        self.finished = False
        self.printouts = printouts

    def guess(self, word):
        if word not in self.validwords_corpus:
            self.print_invalid_word(word)
            return
        self.guesses.append(word)
        if word == self.answer:
            self.finish()
        self.print_self()

    def finish(self):
        self.finished = True
        self.print_finished()
    
    def __str__(self):
        result = ''
        for guess in self.guesses:
            to_print = ''
            for idx, letter in enumerate(guess):
                if letter == self.answer[idx]:
                    to_print += greensquare
                elif letter in self.answer:
                    to_print += orangesquare
                else:
                    to_print += blanksquare
            result += to_print + f' {guess}\n'
        return result[:-1] # removes trailing '\n'

    def get_greens_oranges_blanks(self):
        greens, oranges, blanks = set(), set(), set()
        for guess in self.guesses:
            for idx, letter in enumerate(guess):
                letter_dict = LetterAndPosition(letter, idx)
                if letter == self.answer[idx]:
                    greens.add(letter_dict)
                elif letter in self.answer:
                    oranges.add(letter_dict)
                else:
                    blanks.add(LetterAndPosition(letter, -1))
        return greens, oranges, blanks
        
    def next_valid_words(self):
        result = self.validwords_corpus
        greens, oranges, blanks = self.get_greens_oranges_blanks()
        for green in greens:
            result = list(filter(lambda word: word[green.position] == green.letter, result))
        for orange in oranges:
            result = list(filter(lambda word: word[orange.position] != orange.letter, result))
        for orange in oranges:
            result = list(filter(lambda word: orange.letter in word, result))
        for blank in blanks:
            result = list(filter(lambda word: blank.letter not in word, result))
        return result
    
    def print_next_valid_words(self):
        if not self.printouts: return
        next_valid_words = self.next_valid_words()
        print(f'{len(next_valid_words)} valid words left (printing first 100): {next_valid_words[:100]}')
    
    def print_absent_letters(self):
        if not self.printouts: return
        _, _, blanks = self.get_greens_oranges_blanks()
        print(f'Letters absent: {list(sorted([b.letter for b in blanks]))}')

    def print_finished(self):
        if not self.printouts: return
        print(f'Finished in {len(self.guesses)} moves')
    
    def print_invalid_word(self, word):
        if not self.printouts: return
        print(f'Invalid word: {word}')
    
    def print_self(self):
        if not self.printouts: return
        print(self)
