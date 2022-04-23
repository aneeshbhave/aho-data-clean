import ahocorasick, random


def CleanData(data : str) -> str:
    return data.replace(' ', '').replace('-', '')[-10:]

def MatchText(pool : str, dict : list) -> list:
    a = ahocorasick.Automaton()
    i = 0
    for element in dict:
        a.add_word(element, (i, element))
        i += 1
    a.make_automaton()
    for endIdx, (insertOrder, originalValue) in a.iter(pool):
        startIdx = endIdx - len(originalValue) + -1
        print((startIdx, endIdx), (insertOrder, originalValue))


dict = open("./dict.txt", 'r')
arr = dict.read().splitlines()

pool = open("./pool.txt", 'r')
poolText = pool.read()

MatchText(poolText, arr)


