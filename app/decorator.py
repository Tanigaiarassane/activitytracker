def first():
    print "Into first"
    def second():
        print "Into second"
    return second

def one():
    print "one"

def two():
    print "Two"

def three(f):
    return f()

# Simple decorator

def dec_func(func):
    def wrapper(*args, **kwargs):
        print "Before the function call"
        func(*args, **kwargs)
        print "After the function call"
    return wrapper

@dec_func
def testing(name):
    print "{} - is  a test engineer".format(name)


if __name__== "__main__":

    '''
    f1 = first()
    f1()
    '''

    '''
    three(one)
    three(two)
    '''
    '''
    my_func = dec_func(testing)
    my_func
    '''
    testing('tanigai')