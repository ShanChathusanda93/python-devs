# from filehandler.FileDetector import FileDetector
# from stringfinder.NavigationLinksDetector import NavigationLinksDetector
#
# file_detector = FileDetector()
# nav_links_detector = NavigationLinksDetector()
# file_list = file_detector.get_source_file_paths("/opt/lampp/htdocs/Blog")
# nav_files_details = file_detector.get_navigation_files_details(file_list)
# navigation_details = nav_links_detector.get_navigation_links(nav_files_details)
# navigated_files = nav_links_detector.get_navigated_file_paths(navigation_details, file_list)
# for nav_file in navigated_files:
#     print("==============================")
#     print(nav_file.nav_file_name)
#     print("==============================")
#     for nav_link in nav_file.navigations:
#         print(nav_link)
#         # matching = [file for file in file_list if nav_link in file]
#         # for match in matching:
#         #     print(match)

# import shutil
# import os
# from stringfinder.ReferenceFinder import ReferenceFinder
#
# reference_finder = ReferenceFinder()
# media_files = reference_finder.get_media_references("/opt/lampp/htdocs/Blog/Frontend/frontend.php",
#                                                     "/opt/lampp/htdocs/Blog")
# for media in media_files:
#     file_name = os.path.basename(media)
#     shutil.copy2(media, "/home/shan/Developments/Projects/research-devs/python-devs/stringfinder/created_files/"
#                  + file_name)
# print(file_name)

# from stringfinder.ReferenceFinder import ReferenceFinder
#
# ref = ReferenceFinder()
# with open("/opt/lampp/htdocs/Blog/Frontend/frontend.php", "r") as file:
#     src = file.read().replace("\n", " ")
# php = ref.get_php_occurrences(src)
# incl = ref.get_included_php_file_paths(php, "/opt/lampp/htdocs/Blog", True)
# for inc in incl:
#     print(inc)

# from stringfinder.source_replacer import SourceReplacer
#
# source_replacer = SourceReplacer()
# with open("/opt/lampp/htdocs/Blog/Frontend/frontend.php", "r")as file:
#     source = file.read().replace("\n", " ")
# source_replacer.replace_media_references(source, "/opt/lampp/htdocs/Blog/Frontend/frontend.php",
#                                          "/opt/lampp/htdocs/Blog")

from TestFiles.test_a import A

a = A()
print(a.get_source_path())
