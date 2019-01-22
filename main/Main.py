import os

from fileHandler.FileDetector import FileDetector
from fileHandler.FileParser import conversion_format_detector
from stringFinder.ReferenceFinder import ReferenceFinder

file_detector = FileDetector()
reference_finder = ReferenceFinder()

# --base path of the source files (user inputs)
baseSourcePath = "/home/shan/Developments/Projects/research-devs/Blog"
# --tables which contains the user details (user inputs)
user_tables = ["user_login", "userimage"]

# --calling to the function detect_files to get all the files in the base source path
file_list = file_detector.detect_files(baseSourcePath)

# --detect the access files like login, signup and database connections
access_file_list = file_detector.detect_access_files(file_list, user_tables)

other_files = []
for file in file_list:
    if not any(file in files for files in access_file_list):
        other_files.append(file)

reference_finder.references_detector(other_files, access_file_list, baseSourcePath)

with open("/home/shan/Developments/Projects/research-devs/python-devs/stringFinder/created_files/includeFileList.txt"
        , "r") as incl_files:
    included_files = incl_files.read().splitlines()

# --get the target type of the included files which want to convert
file_detail_list = conversion_format_detector(included_files)

# --separating the files to two lists
article_files = []
separate_files = []
for file in file_detail_list:
    if file.__contains__("article : "):
        article = file.replace("article : ", "")
        article_files.append(article)
    elif file.__contains__("separate : "):
        separate = file.replace("separate : ", "")
        separate_files.append(separate)

for separate_file in separate_files:
    if os.path.exists(separate_files):
        with open(separate_file, "r") as sep_file:
            sep_source = sep_file.read().replace("\n", " ")
        included_files = reference_finder.include_detector(sep_source, source_dir_path="", need_compl_path=False)
        if included_files.__len__() > 0:
            for included_file in included_files:
                print(included_file)

for article_file in article_files:
    if os.path.exists(article_file):
        with open(article_file) as art_file:
            art_source = art_file.read().replace("\n", " ")
        php_occurrences = reference_finder.php_detector(art_source)
        included_files = reference_finder.include_detector(php_occurrences, source_dir_path=" ", need_compl_path=False)
        if included_files.__len__() > 0:
            for included_file in included_files:
                if any("/" + included_file in i for i in article_files):
                    file_name = os.path.splitext(included_file)
                    for occur in php_occurrences:
                        if included_file in occur:
                            occur_words = str(occur).split()
                            old = "<?php" + str(occur) + "?>"
                            replacement = "{article " + file_name[0] + "}\n[introtext]\n[fulltext]\n{/article}"
                            if occur_words.__len__() == 2:
                                art_source = art_source.replace(old, replacement)
                            else:
                                art_source = art_source.replace(occur, replacement)
                elif any("/" + included_file in j for j in separate_files):
                    for occur in php_occurrences:
                        if included_file in occur:
                            art_source = art_source.replace(occur, "include 'file_path_to/" + included_file + "';")

# --next, do the process according to the target file type
