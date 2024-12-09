list1 = [1, 2, 3]
dict1 = {"id": 1}
dict1["permission"] = list1
print(dict1)
list1.append(4)
dict1["id"] = 2
dict2 = dict1
print(dict2)
