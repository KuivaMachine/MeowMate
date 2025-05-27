def spin(input):
    words = input.split()
    newWords = [word[::-1]if len(word)>=5 else word for word in words]
    return " ".join(newWords)

print(spin('hello my dear friends'))