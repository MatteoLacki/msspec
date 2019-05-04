def mix(m,n):
    """Mix lists of tuples with two elements.

    Args:
        m (iterable): A list of tuples
        n (iterable): A list of tuples
    """
    try:
        A = iter(n)
        B = iter(m)
        a = next(A)
        b = next(B)
        while True:
            if a[0] < b[0]:
                yield a
                a = next(A)
            elif b[0] < a[0]:
                yield b
                b = next(B)
            else:
                yield (a[0], a[1]+b[1])
                a = next(A)
                b = next(B)
    except StopIteration:
        pass
    yield from A
    yield from B
