list1 = ["aaaa", "ssss", "dddd", "aaaa", "aaaaa", "gggg", "ssss"]
list2 = ["aaaa", "dddd", "ssss"]
second_list = []
for word in list1:
    if not any(word in a_file for a_file in list2):
        second_list.append(word)
    # if any(word in wordList for wordList in second_list):
    #     second_list.append(word)
for sec in second_list:
    print(sec)
