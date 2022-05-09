a = dict()
user_id = 1234
a[user_id] = list()
user_id = 4321
a[user_id] = list()
print(a)
for i in range(3):
    a[user_id].append(i)
print(a)

b={3424:["otvet1","otvet2"]}
print(b[3424][1])