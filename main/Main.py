from fileHandler.FileDetector import FileDetector
from stringFinder.ReferenceFinder import ReferenceFinder

file_detector = FileDetector()
reference_finder = ReferenceFinder()

file_list = file_detector.detect_files("/home/shan/Developments/Projects/research-devs/Blog")
access_file_list = file_detector.detect_access_files(file_list, "user_login")
for file in access_file_list:
    print(file)
# other_files = []
# for file in file_list:
#     if not any(file in files for files in access_file_list):
#         other_files.append(file)
# reference_finder.references_detector(other_files, access_file_list)
