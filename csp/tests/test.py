def main():
    mul = 3

    def test(number):
        for i in range(10):
            print(number * mul)

    implement(test)

def implement(func):
    func(2)

main()
