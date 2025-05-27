def cipher (input):
    words = input.split()
    letters= [list(word) for word in words]
    for letter in letters:
         [process(let) for let in letter]
    result = [ "".join(word) for word in letters]
    return " ".join(result)


def process(letter):
    return chr(ord(letter)+13)



print(cipher('word dsf  ef!!'))
