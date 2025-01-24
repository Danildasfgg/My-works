def add(a, d):
    return a + d
def subtract(a, d):
    return a - d
def multiply(a, d):
    return a * d
def diving(a ,d):
    return a / d
action = input("Выберите действие (сложить, вычесть, умножить, делить)")
number_1 = int(input("Введите первое число"))
number_2 = int(input("Введите второе число"))
if action == "сложить":
    result = add(number_1, number_2)
    print(result)
else:
    if action == "вычесть":
        result = subtract(number_1, number_2)
        print(result)
    else:
        if action == "умножить":
            result = multiply(number_1, number_2)
            print(result)
        else:
            if action == "делить":
                result = diving(number_1, number_2)
                print(result)

