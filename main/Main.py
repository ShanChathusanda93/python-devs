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

# --get the target type of the files which want to convert
file_detail_list = conversion_format_detector(included_files)

articles = []
separate_files = []
for file in file_detail_list:
    if file.__contains__("article : "):
        article = file.replace("article : ", "")
        articles.append(article)
    elif file.__contains__("separate : "):
        separate = file.replace("separate : ", "")
        separate_files.append(separate)

# --next, do the process according to the target file type
