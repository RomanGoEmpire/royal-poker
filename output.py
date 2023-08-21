def get_input():
    combination = input('Enter your combination: \n').upper()
    if len(combination) != 5:
        print('Invalid input')
        return get_input()
    if not all([card in 'AKQJT' for card in combination]):
        print('Invalid input')
        return get_input()
    return combination

ranking = ['A', 'K', 'Q', 'J', 'T']

def sort_combination(combination):
    return sorted(combination, key=lambda card: ranking.index(card))

def open_file(file):
    with open(file, 'r') as f:
        lines = f.readlines()
    return lines

def get_information(lines, combination):
    for line in lines:
        if line.startswith(combination):
            return line.split(',')
    return None

def get_output(file):
    combination = get_input()
    combination = ''.join(sort_combination(combination))
    lines = open_file(file)
    information = get_information(lines, combination)
    if information:
        print('Information about {}'.format(combination))
        print('Hand: {}'.format(information[0]))
        print('Played: {}'.format(information[1]))
        print('Won: {}'.format(information[2]))
        print('Even: {}'.format(information[3]))
        print('Lost: {}'.format(information[4]))
    else:
        print('No information about {}'.format(combination))


if __name__ == '__main__':
    while True:
        #get_output('3_postflop.csv')
        get_output('5_postflop.csv')
        print()

