import ahocorasick, json

def Main(request):
    dict = ["aneesh", "bhave", "archis"]
    pool = "aneesh archis bhave"
    MatchAho(dict, pool)

def Clean(data :str) -> str:
    return data.replace(' ', '').replace('-', '')[-10:]

def MatchAho(dict :list, pool :str):
    aho = ahocorasick.Automaton()
    
    for i in range(len(dict)):
        aho.add_word(dict[i], (i, dict[i]))

    
    aho.make_automaton()

    print(pool)
    for j, (idx, originalValue) in aho.iter(pool):
        i = j - len(originalValue) + 1
        print(f"{originalValue} from {i} to {j} with insert order of {idx}")
        # assert pool[i:i + len(originalValue)] == originalValue

if __name__ == "__main__":
    Main(None)
