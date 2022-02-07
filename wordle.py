from random import sample
import matplotlib.pyplot as plt
import numpy as np
from game import Game
from players import PlayerBuilder
from corpus import validwords_corpus, answers_corpus

if __name__ == '__main__':
    player_classes = ['NaivePlayer', 'RandomPlayer', 'LetterFrequencyPlayer']
    player_builder = PlayerBuilder()
    for player_class in player_classes:
        histogram = {}
        results = []
        iterations = 10000
        printouts = False
        for i in range(iterations):
            target = sample(answers_corpus, 1)[0]
            game = Game(validwords_corpus, target, printouts)
            player = player_builder.build(player_class, game, validwords_corpus, printouts)
            moves = player.play()
            results.append(moves)
            histogram[moves] = histogram.get(moves, 0) + 1
        avg_result = np.mean(results)
        plt.clf()
        plt.hist(results, bins=np.arange(len(np.bincount(results)))-0.5, rwidth=0.8, density=True)
        plt.xticks(ticks=np.arange(min(results), max(results)+1, 1))
        axes = plt.gca()
        axes.yaxis.grid(color='gray', linestyle=':', linewidth=1)
        plt.xlabel('Number of steps')
        plt.ylabel('Probability')
        plt.title(f'{player_class}: avg {avg_result} steps, {iterations} iterations')
        plt.savefig(f'histograms/{player_class}.png')