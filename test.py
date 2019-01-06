

def test1():
    l = list('acc')
    ix = next(i for i, x in enumerate(l) if x == 'b')
    print(ix)

test1()
