from random import sample
from util import get_letter_probability, get_letter_probability_score_for_word


class NaivePlayer:
    def __init__(self, game, validwords_corpus, printouts=True):
        self.game = game
        self.validwords_corpus = validwords_corpus
        self.printouts = printouts

    def play(self):
        while not self.game.finished:
            guess = self.game.next_valid_words()[0]
            self.game.guess(guess)
            if self.printouts:
                self.game.print_absent_letters()
                self.game.print_next_valid_words()
        return len(self.game.guesses)

    def __str__(self):
        return 'NaivePlayer'


class RandomPlayer:
    def __init__(self, game, validwords_corpus, printouts=True):
        self.game = game
        self.validwords_corpus = validwords_corpus
        self.printouts = printouts

    def play(self):
        while not self.game.finished:
            guess = sample(self.game.next_valid_words(), 1)[0]
            self.game.guess(guess)
            if self.printouts:
                self.game.print_absent_letters()
                self.game.print_next_valid_words()
        return len(self.game.guesses)

    def __str__(self):
        return 'RandomPlayer'


class LetterFrequencyPlayer:
    def __init__(self, game, validwords_corpus, letter_probability_model, printouts=True):
        self.game = game
        self.validwords_corpus = validwords_corpus
        self.printouts = printouts
        self.letter_probability_model = letter_probability_model

    def play(self):
        while not self.game.finished:
            guess = self.get_guess()
            self.game.guess(guess)
            if self.printouts:
                self.game.print_absent_letters()
                self.game.print_next_valid_words()
        return len(self.game.guesses)

    def get_guess(self):
        decision_dict = {}
        for word in self.game.next_valid_words():
            decision_dict[word] = get_letter_probability_score_for_word(
                word, self.letter_probability_model)
  #      if self.printouts:
  #          print(
  #              f'LetterFrequencyPlayer DecisionDict: {dict(sorted(decision_dict.items(), key=lambda item: item[1]))}')
        decision = max(decision_dict, key=decision_dict.get)
        return decision

    def __str__(self):
        return 'LetterFrequencyPlayer'


class PlayerBuilder:
    def __init__(self):
        self.letter_probability_model = None
        self.current_corpus = None

    def build(self, player, game, corpus, printouts=True):
        if player == 'NaivePlayer':
            return NaivePlayer(game, corpus, printouts)
        if player == 'RandomPlayer':
            return RandomPlayer(game, corpus, printouts)
        if player == 'LetterFrequencyPlayer':
            if self.letter_probability_model == None or self.current_corpus != corpus:
                self.letter_probability_model = get_letter_probability(corpus)
            return LetterFrequencyPlayer(game, corpus, self.letter_probability_model, printouts)
        raise ValueError(f"Invalid player: {player}")
