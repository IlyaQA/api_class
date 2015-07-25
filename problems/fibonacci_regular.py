def fib(n):
    l = [0]
    a = 0
    b = 1
    for i in range(n):
        l.append(b)
        temp = a + b
        a = b
        b = temp

    return l

print fib(10)