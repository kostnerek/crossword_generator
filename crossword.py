import re
import random
import json
import os;os.system('cls')
def get_correct_word(letter:str, pos:int)->dict:
    global data
    re_pattern = "\\b[a-zA-Z]{number}[{letter}]{num}[a-zA-Z]{zero}\\b".format(letter=letter, number="{"+str(pos)+"}",num="{"+str(1)+"}",zero="{"+str(0)+",}")
    matched_words = []
    for word in data:
        if re.search(re_pattern, word):
            matched_words.append(word)
    #choose random word from matched words
    try:
        picked_word = random.choice(matched_words)
    except:
        return get_correct_word(letter=letter, pos=random.randrange(0,4))
    _word={}
    _word["word"] = picked_word
    _word["definition"] = data[picked_word]
    _word["position"] = pos
    return _word

global data
data=""
with open('wordDataBase.json', encoding='utf8') as json_file:
    data = json.load(json_file)


#main_word = input("Podaj słowo: ")
main_word = "pies"
def get_crossword(main_word:str)->json:
    
    #list with unique random numbers from 0 to 8
    random_numbers = []
    while len(random_numbers) < len(main_word):
        random_number = random.randint(0, len(main_word)-1)
        if random_number not in random_numbers:
            random_numbers.append(random_number)

    #get words with definitions
    words_and_definitions = []
    counter = 0
    for x in random_numbers:
        elem = get_correct_word(main_word[counter], x)
        words_and_definitions.append(elem)
        counter += 1

    offsets_list=[]

    #get biggest offset
    for x in words_and_definitions:
        offsets_list.append(x["position"])
    offsets_list.sort()
    max_offset = offsets_list[-1]


    crossword_data={}
    c=0
    for x in words_and_definitions:
        pos = x["position"]
        uppercase = x["word"][pos].upper()
        word_list = list(x["word"])
        word_list[pos] = uppercase 
        word = "".join(word_list)
        line=[]
        if pos != max_offset:
                for z in range(max_offset-pos):
                    line.append("_")
        for y in range(len(word)):
            line.append(word[y])
        crossword_data[c] = line
        c+=1

    #==========cleanup data
    #determine longest line
    max_line_len = 0
    for x in crossword_data:
        if len(crossword_data[x]) > max_line_len:
            max_line_len = len(crossword_data[x])

    # add empty lines to all lines
    for x in crossword_data:
        if len(crossword_data[x]) < max_line_len:
            for y in range(max_line_len-len(crossword_data[x])):
                crossword_data[x].append("_")


    c=0
    definitions={}
    for x in words_and_definitions:
        definitions[c] = x['definition']
        c+=1

    all_data_parsed = {}
    all_data_parsed["lines"] = crossword_data
    all_data_parsed['definitions'] = definitions

    additional_data = {}
    additional_data['height'] = len(main_word)
    additional_data['width']  = len(crossword_data[0])
    additional_data['main_word'] = main_word
    additional_data['word_offset'] = crossword_data[0].index(main_word[0].upper())

    all_data_parsed['additional_data'] = additional_data

    with open('output.json', 'w', encoding='utf8') as outfile:
        json.dump(all_data_parsed, outfile, ensure_ascii=False)
    return all_data_parsed

def get_rand_word():
    return random.choice(list(data))
