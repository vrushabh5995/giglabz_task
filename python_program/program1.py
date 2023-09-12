
def star(n):
    if n%2==0:
        print("please enter odd number to get result")
    else:
        i = 1
        while i <= (n // 2) + 1:
            space = (n // 2) - i + 1
            stars = 2 * i - 1
            print(" " * space + "*" * stars)
            i += 1
        i = (n // 2)
        while i >= 1:
            space = (n // 2) - i + 1
            stars = 2 * i - 1
            print(" " * space + "*" * stars)
            i -= 1

star(51)
