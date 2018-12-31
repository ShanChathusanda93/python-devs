# --code in this file will detect the duplicate occurrences of a file
from collections import OrderedDict


def duplicate_detector():
    # --remove the duplicate files from the extracted include file path list
    with open("/home/shan/Developments/Projects/research-devs/python-devs/stringFinder/includeFileList.txt",
              "r") as file:
        include_file_list = file.read()
        file_list = "\n".join(list(OrderedDict.fromkeys(include_file_list.split("\n"))))
        cleaned_list = open("/home/shan/Developments/Projects/research-devs/python-devs/stringFinder"
                            "/non_redundant_includes.txt", "w+")
        cleaned_list.write(file_list)

    # --remove the duplicate files fromm the extracted require files
    with open("/home/shan/Developments/Projects/research-devs/python-devs/stringFinder/requiredFileList.txt",
              "r") as file:
        required_file_list = file.read()
        file_list = "\n".join(list(OrderedDict.fromkeys(required_file_list.split("\n"))))
        cleaned_list.write(file_list)
    cleaned_list.close()
