from fileHandler.FileDetector import FileDetector
from stringFinder.NavigationLinksDetector import NavigationLinksDetector

file_detector = FileDetector()
nav_links_detector = NavigationLinksDetector()
file_list = file_detector.detect_files("/opt/lampp/htdocs/Blog")
nav_files_details = file_detector.get_navigation_files_details(file_list)
navigation_details = nav_links_detector.get_navigation_links(nav_files_details)
navigated_files = nav_links_detector.get_navigated_file_paths(navigation_details, "/opt/lampp/htdocs/Blog")
# for nav_file in navigated_files:
#     print("==============================")
#     print(nav_file.nav_file_name)
#     print("==============================")
#     for nav_link in nav_file.navigations:
#         print(nav_link)
