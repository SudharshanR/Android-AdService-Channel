def a(f_in):
    global somevar
    a.tom = 16
    somevar += 1
    another = 12
    res = f_in + 14
    return res

somevar = 27
another = 17
pvar = 16
print 'a() = ', a(pvar)
print a.tom
print somevar
print another
#print res