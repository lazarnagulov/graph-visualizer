def main():
    print("Start main")
    alpha()
    beta()
    print("End main")

def alpha():
    print("In alpha")
    gamma()
    delta(5)
    epsilon(lambda x: x * 2)

def beta():
    print("In beta")
    gamma()
    for i in range(2):
        zeta(i)

def gamma():
    print("In gamma")
    eta()
    if True:
        theta()

def delta(n):
    print(f"In delta with n={n}")
    if n > 0:
        delta(n - 1)
    else:
        iota()

def epsilon(f):
    print("In epsilon")
    result = f(10)
    print(f"Lambda result: {result}")
    kappa(result)

def zeta(i):
    print(f"In zeta with i={i}")
    if i % 2 == 0:
        lambda_func = lambda a, b: a * b
        print(lambda_func(2, 3))
    else:
        iota()

def eta():
    print("In eta")

def theta():
    print("In theta")

def iota():
    print("In iota")
    try:
        kappa(0)
    except Exception as e:
        print(f"Caught exception in iota: {e}")

def kappa(x):
    print(f"In kappa with x={x}")
    if x == 0:
        raise ValueError("Zero not allowed")
    else:
        lambda z: print(f"kappa lambda: {z}")(x)

main()