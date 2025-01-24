kor = int(input("Введите корень"))
if kor < 0:
    result = "Корней нет"
elif kor == 0:
    result = "Один корень"
elif kor > 0:
    result = "Два корня"
else:
    print("Фигня какая-то")
print(result)