count = 0
for i in range(int(input())):
    number = int(input())
    if number % 4 == 0 and number % 7 != 0:
        count += 1
print(count)