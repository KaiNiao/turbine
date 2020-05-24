class Sample_1():
    def __enter__(self):
        print("in __enter__")
        return 'Foo'
    
    # TypeError: __exit__() takes 1 positional argument but 4 were given
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("in __exit__")
        print("exc_type", exc_type)  # exc_type None 
        print("exc_val", exc_val)  # exc_val None
        print("exc_tb", exc_tb)  # exc_tb None


def get_sample_1():
    return Sample_1()


with get_sample_1() as sample:
    print(sample)


class Sample_2():
    def __enter__(self):
        print("in __enter__")
        return self
    
    # TypeError: __exit__() takes 1 positional argument but 4 were given
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("in __exit__")
        print("exc_type", exc_type)
        print("exc_val", exc_val)
        print("exc_tb", exc_tb)

    def do_something(self):
        result = 1 / 0
        return result
    

def get_sample_2():
    return Sample_2()


with get_sample_2() as sample:
    sample.do_something()