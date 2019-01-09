from fileHandler.FileDetector import FileDetector

fileDetector = FileDetector()
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
with open("/home/shan/Developments/Projects/research-devs/python-devs/main/sourceList.txt", "r") as source_files:
    file_list = source_files.read().splitlines()
fileDetector.detect_access_files(file_list, "user_login")
