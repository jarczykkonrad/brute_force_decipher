import itertools
import freqAnalysis
import time


NUM_MOST_FREQ_LETTERS = 4

cipher="FRRPU TIIYE AMIRN QLQVR BOKGK NSNQQ IUTTY\
        IIYEA WIJTG LVILA ZWZKT ZCJQH IFNYI WQZXH\
        RWZQW OHUTI KWNNQ YDLKA EOTUV XELMT SOSIX\
        JSKPR BUXTI TBUXV BLNSX FJKNC HBLUK PDGUI\
        IYEAM OJCXW FMJVM MAXYT XFLOL RRLAA JZAXT\
        YYWFY NBIVH VYQIO SLPXH ZGYLH WGFSX LPSND\
        UKVTR XPKSS VKOWM QKVCR TUUPRWQMWY XTYLQ\
        XYYTR TJJGO OLMXV CPPSL KBSEI PMEGC RWZRI\
        YDBGE BTMFP ZXVMF MGPVO OKZXX IGGFE SIBRX\
        SEWTY OOOKS PKYFC ZIEYF DAXKG ARBIW KFWUA\
        SLGLF NMIVH VVPTY IJNSX FJKNC HBLUK PDGUI\
        IYEAM HVFDY CULJS EHHMX LRXBN OLVMR"

dict1 = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4,
         'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9,
         'K': 10, 'L': 11, 'M': 12, 'N': 13, 'O': 14,
         'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19,
         'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24, 'Z': 25}

dict2 = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E',
         5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J',
         10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O',
         15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T',
         20: 'U', 21: 'V', 22: 'W', 23: 'X', 24: 'Y', 25: 'Z'}

def erase_spaces(with_spaces):
    no_spaces = ""
    for letter in with_spaces:
        if letter == " ":
            no_spaces+=''
        else:
            no_spaces+=letter
    return no_spaces

def vigenere_decipher(key, cipher):
    LETTERS ="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    plaintext = []
    index=0
    for letter in cipher:
        num = LETTERS.find(letter.upper())
        if num != -1:
            num -= LETTERS.find(key[index])
            num %= len(LETTERS)
            if letter.isupper():
                plaintext.append(LETTERS[num])
            elif letter.islower():
                plaintext.append(letter[num].lower())
            index += 1
            if index == len(key):
                index = 0
        else:
            plaintext.append(letter)

    return ''.join(plaintext)

def autokey_decypher (key, cipher):
    message = ''
    i = 0
    original_key = key
    for letter in cipher:
        if letter == ' ':
            message += ''
        else:
            x = (dict1[letter]-dict1[key[i]]+26) % 26
            i+=1
            key+=dict2[x]
            message += dict2[x]
    key = key[:len(key)-len(original_key)]
    return message

def trigramCount(message):
    trigramsFile = open('trigrams.txt')
    trigrams = {}
    for word in trigramsFile.read().split('\n'):
        word = word.upper()
        trigrams[word] = None
    trigramsFile.close()
    possibleWords = message.split()
    if possibleWords == []:
        return 0.0
    matches = 0
    for word in possibleWords:
        if word in trigrams:
            matches += 1
    return float(matches) / len(possibleWords)

def check_if_text(string, wordPercentage=5):
    #spliting string into 3 variables with 3 character length
    string_1 = ''.join([x + ' ' if i % 3 == 2 else x for i, x in enumerate(string)])
    string_2 = ''.join([x + ' ' if i % 3 == 1 else x for i, x in enumerate(string)])
    string_3 = ''.join([x + ' ' if i % 3 == 0 else x for i, x in enumerate(string)])
    if trigramCount(string_1) * 100 >= wordPercentage:
        return True
    elif trigramCount(string_2) * 100 >= wordPercentage:
        return True
    elif trigramCount(string_3) * 100 >= wordPercentage:
        return True
    else:
        return False

def getNthSubkeysLetters(n, keyLength, message):
    # returns every Nth letter for each keyLength set of letters in text
    i = n - 1
    letters = []
    while i < len(message):
        letters.append(message[i])
        i += keyLength
    return ''.join(letters)

def brute_force(cipher, key_length):
    characters="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    allFreqScores = []

    for nth in range(1, key_length + 1):
        nthLetters = getNthSubkeysLetters(nth, key_length, cipher)
        freqScores = []
        for possibleKey in characters:
            decryptedText = autokey_decypher(possibleKey, nthLetters)
            keyAndFreqMatchTuple = (possibleKey, freqAnalysis.englishFreqMatchScore(decryptedText))
            freqScores.append(keyAndFreqMatchTuple)

        freqScores.sort(key=getItemAtIndexOne, reverse=True)

        allFreqScores.append(freqScores[:NUM_MOST_FREQ_LETTERS])

    for i in range(len(allFreqScores)):
        print('Possible letters for letter %s of the key: ' % (i + 1), end='')
        for freqScore in allFreqScores[i]:
            print('%s ' % freqScore[0], end='')
        print()

    for indexes in itertools.product(range(NUM_MOST_FREQ_LETTERS), repeat=key_length):
        possibleKey=''
        for i in range(key_length):
            possibleKey += allFreqScores[i][indexes[i]][0]
        print('Attempting with key: %s' % (possibleKey))

        decryptedText = autokey_decypher(possibleKey, cipher)

        if check_if_text(decryptedText):
            print('Possible encryption hack with key %s:' % (possibleKey))
            print(decryptedText[:200])
            print()
            end = time.time()
            print("The time of execution of above program is :",
                  (end - start) * 10 ** 3, "ms")
            print('Enter D for done, or just press Enter to continue hacking:')
            response = input('> ')

            if response.strip().upper().startswith('D'):
                return decryptedText

def getItemAtIndexOne(x):
    return x[1]

def hack_autokey(cipher):
    min_key_length = 2
    max_key_length = 10
    cipher_without_spaces = erase_spaces(cipher)
    for keyLength in range(min_key_length, max_key_length+1):
        print('Attempting hack with key length %s (%s possible keys)...' % (keyLength, NUM_MOST_FREQ_LETTERS ** keyLength))
        decryptedText = brute_force(cipher_without_spaces, keyLength)
        if decryptedText != None:
            break
    return decryptedText
if __name__ == '__main__':
    start = time.time()
    decrypted_text = hack_autokey(cipher)
    print(decrypted_text)


