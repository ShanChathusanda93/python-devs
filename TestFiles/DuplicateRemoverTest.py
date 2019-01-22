import re
# list1 = ["aaaa", "ssss", "dddd", "aaaa", "aaaaa", "gggg", "ssss"]
# list2 = ["aaaa", "dddd", "ssss"]
# second_list = []
# for word in list1:
#     if not any(word in a_file for a_file in list2):
#         second_list.append(word)
#     # if any(word in wordList for wordList in second_list):
#     #     second_list.append(word)
# for sec in second_list:
#     print(sec)
#
# with open("/opt/lampp/htdocs/Blog/post views/view_post_image_phpcode.php", "r") as source_file:
#     code = source_file.read()
# source = code.replace("\n", " ")
# extended_ends = re.findall("endwhile;", source)
# search = re.search("while \(", source)
# # for s in search:
# print(search)
# i = extended_ends.__len__()
# for end in extended_ends:
#     source = source.replace("endwhile;", i.__str__(), 1)
#     i = i - 1

# print(source)

# string = "I am a student as well as a teacher"
# occurrences = re.findall("as", string)
# substr = ["xas", "yas"]
# i = 0
# for occur in occurrences:
#     string = string.replace(occur, substr[i])
#     i = i + 1
#
# print(string)

# s = "I am a student as well as a teacher"
# s = s.replace("as", "xxx", 1)
# print(s)
# s = s.replace("as", "yyy", 1)
# print(s)


# --include detection
# import re
#
# string = "include '../Template/Bootstrap/bootstrap.php';"
# included_file = "bootstrap.php"
# reg = r"include(.*?)" + re.escape(included_file) + r"(\"|\');"
# # file = re.findall(r"include(.*?)%s(\"|\');" % included_file, string)
# file = re.findall(reg, string)
# print(file[0])

# --string split
string = "<?php include '../Template/Bootstrap/bootstrap.php'; ?>"
words = string.split()
words.remove("include")
# words.remove("'../Template/Bootstrap/bootstrap.php';")
for word in words:
    print(word)
