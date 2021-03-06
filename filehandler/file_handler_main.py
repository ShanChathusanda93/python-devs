# from filehandler.FileDetector import FileDetector
#
# fileDetector = FileDetector()
# fileDetector.get_source_file_paths("/home/shan/Developments/Projects/research-devs/Blog/", "login")
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
# files = fileDetector.get_user_management_file_paths(file_list, "user_login")
# for file in files:
#     print(file)
# import re
# from filehandler.ConnectionCreator import ConnectionCreator
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


# from filehandler.FileDetector import FileDetector
# from stringfinder.NavigationLinksDetector import NavigationLinksDetector
#
# file_detector = FileDetector()
# navigation_detector = NavigationLinksDetector()
# file_list = file_detector.get_source_file_paths("/opt/lampp/htdocs/Blog")
# nav_files = file_detector.get_navigation_files_details(file_list)
# # for nav in nav_files:
# #     print(nav.nav_file_name)
# #     for navigate in nav.navigations:
# #         print(navigate)
# navigation_links = navigation_detector.get_navigation_links(nav_files, "/opt/lampp/htdocs/Blog")

# from filehandler.FileDetector import FileDetector

# file_detector = FileDetector()
# file_list = file_detector.get_media_file_paths("/opt/lampp/htdocs/Blog")
# for file in file_list:
#     print(file)
# print(file_list.__len__())

# from filehandler.file_migrator import FileMigrator
#
# file_migrator = FileMigrator()
# file_migrator.move_media_files("/opt/lampp/htdocs/Blog/Frontend/frontend.php", "/opt/lampp/htdocs/Blog")

from filehandler.file_detector import FileDetector
from stringfinder.navigation_links_detector import NavigationLinksDetector
from stringfinder.reference_finder import ReferenceFinder
from stringfinder.include_tree_detector import incl_tree

file_detector = FileDetector()
nav_link_detector = NavigationLinksDetector()
reference_finder = ReferenceFinder()
file_list = file_detector.get_source_file_paths("/opt/lampp/htdocs/Blog")
# navigation_file_list = ["/opt/lampp/htdocs/Blog/Template/Navigation/frontend_navigation.php",
#              "/opt/lampp/htdocs/Blog/Template/Navigation/profile_navigation.php",
#              "/opt/lampp/htdocs/Blog/Template/Navigation/profile_navigation_home.php"]
navigation_file_list = ["/opt/lampp/htdocs/Blog/Template/Navigation/frontend_navigation.php"]
nav_file_details = file_detector.get_navigation_files_details(navigation_file_list)
nav_details = nav_link_detector.get_navigation_links(nav_file_details)
nav_links = nav_link_detector.get_navigated_file_paths(nav_details, file_list)
for nav in nav_links:
    print("===============")
    print(nav.get_nav_file_name())
    print("===============")
    for det in nav.get_navigations():
        has_incl = reference_finder.has_include(det)
        print(det)
        if has_incl == 1:
            incl_tree(det, "/opt/lampp/htdocs/Blog")
        else:
            print("===file has no included files")

# for nav in nav_links:
#     print("===============")
#     print(nav.get_nav_file_name())
#     print("===============")
#     for det in nav.get_navigations():
#         print("\t" + det)
