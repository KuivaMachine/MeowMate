def solution(number):
    numsSet = set()
    num=number-1
    while not num<3:
        if num%3==0 or num%5==0:
            numsSet.add(num)
        num-=1
    return sum(numsSet)
    

number =200
print(solution(number-1))