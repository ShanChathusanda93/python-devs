# --This file contains the code for accessing another function of another python file. --in order to import a file
# from another directory, that directory should be a module. Otherwise it will not detect the functions of that
# file/class
# from fileHandler.FileDetector import FileDetector

# --creating the instance from the imported class
# fileDetector = FileDetector
# --Here we need to send the instance alongside with the other required arguments to the function
# fileDetector.detect_files(fileDetector, "/home/shan/Developments/Projects/research-devs/Blog/", "login")

# --this code segment is for reading the files
# with open("/home/shan/Developments/Projects/research-devs/Blog/post views/wastet/posttext.php", "r") as file:
#     src = file.read()
#     print(src.__len__())

# import pathlib
#
# path = pathlib.Path(r"/home/shan/Developments/Projects/research-devs/Blog/Frontend/frontend.php")
# dirPath = path.parent
# print(dirPath)

# --following code can detect the directory path of a source file
# import os
#
# path = r"/home/shan/Developments/Projects/research-devs/Blog/Frontend/frontend.php"
# dirPath = os.path.dirname(path)
# print(dirPath)

# from stringFinder.ReferenceFinder import ReferenceFinder
#
# ref_det = ReferenceFinder
# ref_det.reference_detector(ref_det)

# import re
#
# path = "/home/shan/Developments/Projects/research-devs/Blog/User/user profile detail/edit_profile.php"
# with open(path, "r") as file:
#     orig = file.read()
#     text = orig.replace("\n", " ")
# # pattern = re.compile(r'/\*\*.+?\*/', re.DOTALL)
# # pattern.search(text).group()
#
# cmnts = re.search(r'(\/*(.|[\r\n])*?(\*\/))', orig)
# print(cmnts.group(0))

from stringFinder.DuplicateFileDetector import duplicate_detector
from stringFinder.ReferenceFinder import ReferenceFinder

# duplicate_detector()
ref_find = ReferenceFinder
file = open("/home/shan/Developments/Projects/research-devs/python-devs/stringFinder/non_redundant_includes.txt", "r")
files = file.read().splitlines()
values = ref_find.has_include(ref_find, files)
for file_list in values:
    for f in file_list:
        print(f)
    print("\n")
