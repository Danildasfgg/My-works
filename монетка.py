import random, time
print("Монетка падает")
time.sleep(5)
random11 = random.randint(0, 1000)
if random11 >= 500:
    print("Выпала орел")
else:
    print("Выпала решка")