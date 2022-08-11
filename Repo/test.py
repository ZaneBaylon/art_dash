def hello():
    print("hello")

class testClass:
    
    def __init__(self, one, two):
        self.one = one
        self.two = two
        print1 = self.function1(one)
        print2 = self.function2(two)
        self.add(print1, print2)
    
    def function1(self, one):
        print(one)
        if one == "1":
            return True
        else:
            return False

    def function2(self, two):
        print(two)
        if two == "2":
            return True
        else:
            return False

    def add(self, print1, print2):
        if print1 == print2:
            print("same")
        else:
            print('diff')
    
testClass('1','2')

