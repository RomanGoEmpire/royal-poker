import itertools

suits = ['A', 'K', 'Q', 'J', 'T']

combinations = list(itertools.combinations_with_replacement(suits, 6))
combinations = [combination for combination in combinations if combination.count('A') <= 4]
combinations = [combination for combination in combinations if combination.count('K') <= 4]
combinations = [combination for combination in combinations if combination.count('Q') <= 4]
combinations = [combination for combination in combinations if combination.count('J') <= 4]
combinations = [combination for combination in combinations if combination.count('T') <= 4]
print(combinations)
print(len(combinations))
for combination in combinations:
    print(''.join(combination))

