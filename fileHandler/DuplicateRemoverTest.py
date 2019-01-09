list = ["aaaa", "ssss", "dddd", "aaaa", "aaaaa", "gggg", "ssss"]
second_list = []
for word in list:
    if not any(word in a_file for a_file in second_list):
        second_list.append(word)

for sec in second_list:
    print(sec)
