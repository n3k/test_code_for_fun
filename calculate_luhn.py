def calculate_luhn(number):
    a = str(number)[:-1]
    a = [int(_) for _ in a[::-1]]
    for i in xrange(len(a)):
        if not i&1:
            a[i] = a[i] * 2
            if a[i] > 9:
                a[i] = a[i] - 9
    result = sum(a)
    print result, result%10
