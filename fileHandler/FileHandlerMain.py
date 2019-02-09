# from fileHandler.FileDetector import FileDetector
#
# fileDetector = FileDetector()
# fileDetector.detect_files("/home/shan/Developments/Projects/research-devs/Blog/", "login")
# file_list = ["/home/shan/Developments/Projects/research-devs/Blog/Login System/login_phpcode.php",
#              "/home/shan/Developments/Projects/research-devs/Blog/Login System/register_phpcode.php",
#              "/home/shan/Developments/Projects/research-devs/Blog/Login System/login.php",
#              "/home/shan/Developments/Projects/research-devs/Blog/Login System/register.php",
#              "/home/shan/Developments/Projects/research-devs/Blog/Login System/login_form.php",
#              "/home/shan/Developments/Projects/research-devs/Blog/Login System/register_form.php",
#              "/home/shan/Developments/Projects/research-devs/Blog/Login System/sign_form.php",
#              "/home/shan/Developments/Projects/research-devs/Blog/Login System/sign_phpcode.php",
#              "/home/shan/Developments/Projects/research-devs/Blog/Login System/logout.php",
#              "/home/shan/Developments/Projects/research-devs/Blog/Login System/config.php"]
# with open("/home/shan/Developments/Projects/research-devs/python-devs/main/sourceList.txt", "r") as source_files:
#     file_list = source_files.read().splitlines()
# files = fileDetector.detect_access_files(file_list, "user_login")
# for file in files:
#     print(file)
# import re
# from fileHandler.ConnectionCreator import ConnectionCreator
#
# con_creator = ConnectionCreator()
# with open("/opt/lampp/htdocs/Blog/Login System/config.php", "r") as file:
#     source = file.read().replace("\n", " ")
# words = source.split(";")
# # for word in words:
# match = [s for s in words if "mysqli_connect(" in s]
# # print(match[0])
# connection_var = re.findall("\$(.*?)=", match[0])
# # print(connection_var[0])
# con_creator.create_database_connection_file(connection_var[0], server_name="myserver", username="myuname",
#                                             password="mypass", db_name="mydb")


from fileHandler.FileDetector import FileDetector

file_detector = FileDetector()
file_list = file_detector.detect_files("/opt/lampp/htdocs/Blog")
nav_files = file_detector.get_navigation_files_details(file_list)
for nav in nav_files:
    print(nav.nav_file_name)
    for navigate in nav.navigations:
        print(navigate)
