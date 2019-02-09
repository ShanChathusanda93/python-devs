import os

from codeparser.CodeFormatter import format_code
from fileHandler.ConnectionCreator import ConnectionCreator
from fileHandler.DirMaker import DirectoryMaker
from fileHandler.FileDetector import FileDetector
from fileHandler.FileParser import conversion_format_detector
from stringFinder.HeaderRemover import remove_html_header
from stringFinder.LoopDetector import LoopDetector
from stringFinder.ReferenceFinder import ReferenceFinder

file_detector = FileDetector()
reference_finder = ReferenceFinder()
loop_detector = LoopDetector()
dir_maker = DirectoryMaker()
con_creator = ConnectionCreator()

# --base path of the source files (user inputs)
baseSourcePath = "/home/shan/Developments/Projects/research-devs/Blog"
# --tables which contains the user details (user inputs)
user_tables = ["user_login", "userimage"]

# --calling to the function detect_files to get all the files in the base source path
file_list = file_detector.detect_files(baseSourcePath)

# --detect the access files like login, signup and database connections
access_file_list = file_detector.detect_access_files(file_list, user_tables)
database_connect_file_path = file_detector.get_database_connect_file_name(file_list)
database_connect_file = " "
if database_connect_file_path.__len__() == 1:
    # --user inputs
    server_name = "myserver"
    username = "myuname"
    password = "mypass"
    db_name = "mydb"
    # --
    database_connect_file = os.path.basename(database_connect_file_path[0])
    connection_var = con_creator.get_connection_variable(database_connect_file_path[0])
    con_creator.create_database_connection_file(connection_var, server_name, username, password, db_name)
elif database_connect_file_path.__len__() > 1:
    print("Error, there are two or more database connection files.")

# other_files = []
# for file in file_list:
#     if not any(file in files for files in access_file_list):
#         other_files.append(file)

# --get the files which have the content of the web application
content_files = file_detector.get_content_files(file_list, access_file_list)

reference_finder.references_detector(content_files, access_file_list, baseSourcePath)

with open("/home/shan/Developments/Projects/research-devs/python-devs/stringFinder/created_files/includeFileList.txt",
          "r") as incl_files:
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

article_files = ["/opt/lampp/htdocs/Blog/post views/view_post_image_phpcode.php"]
for article_file in article_files:
    if os.path.exists(article_file):
        with open(article_file) as art_file:
            art_source = art_file.read().replace("\n", " ")
        # --get the file name of the article file
        tempBasePath = os.path.basename(article_file)
        art_file_name = os.path.splitext(tempBasePath)[0].replace(' ', '_')

        php_occurrences = reference_finder.php_detector(art_source)
        included_files = reference_finder.include_detector(php_occurrences, source_dir_path=" ", need_compl_path=False)
        if included_files.__len__() > 0:
            for included_file in included_files:
                if database_connect_file in included_file:
                    db_connection = "/home/shan/Developments/Projects/research-devs/python-devs/fileHandler" \
                                    "/phpSnippets/dbconnection/connection.php"
                    art_source = art_source.replace(included_file, db_connection)
                else:
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

        required_files = reference_finder.require_detector(php_occurrences, source_dir_path=" ", need_compl_path=False)
        if required_files.__len__() > 0:
            for required_file in required_files:
                if database_connect_file in required_file:
                    db_connection = "/home/shan/Developments/Projects/research-devs/python-devs/fileHandler" \
                                    "/phpSnippets/dbconnection/connection.php"
                    art_source = art_source.replace(required_file, db_connection)
                else:
                    if any("/" + required_file in k for k in article_files):
                        base_name = os.path.basename(required_file)
                        file_name = os.path.splitext(base_name)
                        occur = " "
                        for occur in php_occurrences:
                            if required_file in occur:
                                occur_words = str(occur).splitlines()
                                old = "<?php" + str(occur) + "?>"
                                replacement = "{article " + file_name[0] + "}\n[introtext]\n[fulltext]\n{/article}"
                                if occur_words.__len__() == 2:
                                    art_source = art_source.replace(old, replacement)
                                else:
                                    art_source = art_source.replace(occur, replacement)
                    elif any("/" + required_file in m for m in separate_files):
                        for occur in php_occurrences:
                            if required_file in occur:
                                art_source = art_source.replace(occur, "include 'file_path_to/required_file.php';")

        art_source = loop_detector.detect_extended_while_loops(art_source, art_file_name)
        php_occurrences = reference_finder.php_detector(art_source)
        i = 0
        for occur in php_occurrences:
            words = str(occur).split()
            if words.__len__() > 2:
                i = i + 1
                target_dir_path = "/home/shan/Developments/Projects/research-devs/python-devs/fileHandler/phpSnippets" \
                                  + "/" + art_file_name
                dir_maker.make_directory(target_dir_path)
                target_file_path = target_dir_path + "/" + art_file_name + "_php_partition_" + i.__str__() + ".php"
                with open(target_file_path, "w") as file:
                    file.write("<?php \n" + occur + " \n?>")
                art_source = art_source.replace(occur, " include \"" + target_file_path + "\";")
        art_source = remove_html_header(art_source)
        art_source = format_code(art_source)
        print(art_source)

# --next, do the process according to the target file type
