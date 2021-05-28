

def fizzBuzz(n):
    # Write your code here
    for i in range(1, n + 1):
        print(i, i %3, i %5, end=" | ")
        if i % 5 == 0 and i % 3 == 0 :
            print("FizzBuzz")
        elif i % 3 == 0 and i % 5 != 0:
            print("Fizz")
        elif i % 5 == 0 and i % 3 != 0:
            print("Buzz")
        else:
            print(i)


if __name__ == '__main__':
    n = 15

    fizzBuzz(n)
