

def decrypt(arr,n):
    return "".join(search(arr, 0,n)[::-1])

def search(arr, level, n, backet=None):
    if backet==None:
        backet=[]
    if level == n:
        for y in arr:
            if isinstance(y,str):
                backet.append(y)
        return backet

    for x in arr:
        if isinstance(x, list):
            search(x,level+1, n,backet)
    return backet

print(decrypt(["a", "b", ["c"], ["world", "hello"]],0))
