from fileHandler.FileDetector import FileDetector

fileDetector = FileDetector()
# fileDetector.detect_files("/home/shan/Developments/Projects/research-devs/Blog/", "login")
file_list = ["/home/shan/Developments/Projects/research-devs/Blog/Login System/login_phpcode.php",
             "/home/shan/Developments/Projects/research-devs/Blog/Login System/register_phpcode.php",
             "/home/shan/Developments/Projects/research-devs/Blog/Login System/login.php",
             "/home/shan/Developments/Projects/research-devs/Blog/Login System/register.php"]
fileDetector.detect_access_files(file_list, "user_login")
