def f(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return f(n-1) + f(n-2)


def seq(n):
    l = []
    for i in range(n):
        l.append(f(i))
    return l

print(seq(16))