def main():
    print("=== Begin Execution ===")
    alpha()
    beta()
    try:
        omega()
    except Exception as e:
        print(f"Exception caught in main: {e}")
    print("=== End Execution ===")

def alpha():
    print("In alpha")
    gamma()
    delta(3)
    epsilon(lambda x: x + 10)
    phi()

def beta():
    print("In beta")
    gamma()
    for i in range(2):
        zeta(i)
    eta()

def gamma():
    print("In gamma")
    theta()
    if True:
        iota()
        upsilon()

def delta(n):
    print(f"In delta({n})")
    if n > 0:
        delta(n - 1)
    else:
        kappa()

def epsilon(fn):
    print("In epsilon")
    result = fn(7)
    print(f"Lambda result in epsilon: {result}")
    lambda x: print("unused lambda")(42)
    lambda_func = lambda y: y * 3
    kappa(lambda_func(result))

def zeta(i):
    print(f"In zeta({i})")
    if i % 2 == 0:
        lambda_func = lambda a, b: a * b
        print(lambda_func(4, 5))
    else:
        iota()
    nested_caller(i)

def eta():
    print("In eta")
    nested_call_chain()

def theta():
    print("In theta")
    iota()

def iota():
    print("In iota")
    try:
        kappa(0)
    except ValueError as ve:
        print(f"Caught error in iota: {ve}")
    finally:
        print("Finally block in iota")

def kappa(x=1):
    print(f"In kappa({x})")
    if x == 0:
        raise ValueError("Zero is not allowed")
    lambda z: print(f"Kappa lambda: {z}")(x)
    return x + 1

def lambda_caller():
    print("In lambda_caller")
    func_list = [
        lambda x: x + 1,
        lambda x: x ** 2,
        lambda x: x - 3
    ]
    for f in func_list:
        print(f(5))

def nested_call_chain():
    print("In nested_call_chain")
    def level1():
        print("In level1")
        def level2():
            print("In level2")
            def level3():
                print("In level3")
                phi()
            level3()
        level2()
    level1()

def nested_caller(val):
    print(f"In nested_caller({val})")
    def choose_path(x):
        if x < 1:
            rho()
        else:
            sigma()
    choose_path(val)

def phi():
    print("In phi")
    chi()
    alpha()

def chi():
    print("In chi")
    psi()

def psi():
    print("In psi")
    omega()

def omega():
    print("In omega")
    alpha()  # mutual recursion
    raise RuntimeError("Intentional error in omega")

def rho():
    print("In rho")
    phi()

def sigma():
    print("In sigma")
    tau()

def tau():
    print("In tau")
    lambda_caller()
    upsilon()

def upsilon():
    print("In upsilon")
    pi()

def pi():
    print("In pi")

main()
