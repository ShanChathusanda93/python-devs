# --This file contains the code for accessing another function of another python file. --in order to import a file
# from another directory, that directory should be a module. Otherwise it will not detect the functions of that
# file/class
# from filehandler.FileDetector import FileDetector

# --creating the instance from the imported class
# fileDetector = FileDetector
# --Here we need to send the instance alongside with the other required arguments to the function
# fileDetector.get_source_file_paths(fileDetector, "/home/shan/Developments/Projects/research-devs/Blog/", "login")

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

# from stringfinder.ReferenceFinder import ReferenceFinder
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

# from stringfinder.ReferenceFinder import ReferenceFinder
#
# # duplicate_detector()
# ref_find = ReferenceFinder
# file = open("/home/shan/Developments/Projects/research-devs/python-devs/stringfinder/non_redundant_includes.txt", "r")
# files = file.read().splitlines()
# values = ref_find.has_include(ref_find, files)
#
# for index, file_list in enumerate(values):
#     if index == 0:
#         print("no_includes_files")
#         for f in file_list:
#             print(f)
#         print(file_list.__len__())
#     elif index == 1:
#         print("has_includes_files")
#         for f in file_list:
#             print(f)
#         print(file_list.__len__())
#     print("\n")

# --test loop detector
# from stringfinder.LoopDetector import LoopDetector
#
# loop_detector = LoopDetector()
# loop_detector.detect_extended_while_loops(source=" ", file_name="view_post_image_phpcode")

# ref = ["abc"]
# some_list = ['abc-123', 'def-456', 'ghi-789', 'abc-456', '452-abc']
# for r in ref:
#     matching = [s for s in some_list if r in s]
#     for match in matching:
#         print(match)
# count = 2
# street_no = {"1": count, "2": "Hansi Mihiravi", "3": "Dana", "4": "Paaru"}
# count = 3
# street_no.update({"1": count})
# if "5" in street_no:
#     print("ok")
# else:
#     print("no")

# print(street_no["2"])
# from filehandler.file_detector import FileDetector
# from dataobjects.detail_keeper_do import DetailsKeeperDO
#
# file_detector = FileDetector()
# file_detector.get_source_file_paths("/opt/lampp/htdocs/Blog")
# print(DetailsKeeperDO.source_dir_path)

# from bs4 import BeautifulSoup
# # import requests
# #
# # source_file = requests.get("/opt/lampp/htdocs/Blog/Template/Navigation/frontend_navigation.php")
# with open("/opt/lampp/htdocs/Blog/Template/Navigation/frontend_navigation.php", "r") as source_file:
#     source = source_file.read().replace("\n", " ")
# print(source)
# print("========")
# soup = BeautifulSoup(source, "html.parser")
# final = soup.prettify()
# with open("final.php", "w") as final_file:
#     final_file.write(final)

# from filehandler.files_dir_maker import FilesNDirectoryMaker
#
# file_maker = FilesNDirectoryMaker()
# file_maker.create_target_file("/opt/lampp/htdocs/new", "/opt/lampp/htdocs/Blog/Template/Navigation/frontend_navigation.php")

from dataobjects.detail_keeper_do import DetailsKeeperDO
# from filehandler.files_dir_maker import FilesDirectoryMaker
#
# # DetailsKeeperDO.set_db_conn_file(DetailsKeeperDO, "/opt/lampp/htdocs/Blog/config/db_conn.php")
# # avoided_file_list = ["/opt/lampp/htdocs/Blog/config/bbbb.php", "/opt/lampp/htdocs/Blog/config/aaaa.php",
# #                      "/opt/lampp/htdocs/Blog/config/cccc.php"]
# # DetailsKeeperDO.set_avoided_file_list(DetailsKeeperDO, avoided_file_list)
# file_maker = FilesDirectoryMaker()
# # file_maker.create_target_file("/opt", "/opt/lampp/htdocs/Blog/config/aaa.php")
# file_maker.create_target_parent_file("/opt/lampp", "/opt/lampp/htdocs/Blog/Frontend/frontend.php")

# from stringfinder.source_replacer import SourceReplacer
#
# src_rpl = SourceReplacer()
# with open("/opt/lampp/htdocs/Blog/Login System/logout.php") as file:
#     src = file.read().replace("\n", " ")
# src = src_rpl.replace_session_start(src)
# print(src)

# --session replacing methods testing
# from stringfinder.source_replacer import SourceReplacer
#
# src_rpl = SourceReplacer()
# with open("/opt/lampp/htdocs/Blog/User/post/post_image_edit.php") as file:
#     src = file.read().replace("\n", " ")
# src = src_rpl.replace_session_start(src)
# src = src_rpl.replace_session_details_assignment(src)
# src_rpl.replace_session_details_extraction(src)
# ---


# --create main module file method testing
# from filehandler.files_dir_maker import FilesDirectoryMaker
#
#
# DetailsKeeperDO.set_source_dir_path(DetailsKeeperDO, "/opt/lampp/htdocs/Blog")
# file_maker = FilesDirectoryMaker()
# file_maker.create_main_module_file("/opt/lampp/htdocs/Blog/TreeTest/a.php")

# --string appending testing
# str_list = ["aaaa.php", "bbb.php", "cccc.php"]
# file_string = ""
# for str in str_list:
#     file_string = file_string + "<filename>" + str + "</filename>\n"
# print(file_string)
