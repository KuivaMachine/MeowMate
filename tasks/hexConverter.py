def rgb(r, g, b):
    return f"{convert(r)}{convert(g)}{convert(b)}"

def convert(num):
    if num<0:
        num=0
    elif num>255:
        num =255
    if num>16:
        return "{:X}".format(num)
    else:
        return "0"+"{:X}".format(num)

print(r)