# --This file contains the code for accessing another function of another python file. --in order to import a file
# from another directory, that directory should be a module. Otherwise it will not detect the functions of that
# file/class
from fileHandler.FileDetector import FileDetector

# --creating the instance from the imported class
fileDetector = FileDetector
# --Here we need to send the instance alongside with the other required arguments to the function
fileDetector.detect_files(fileDetector, "/home/shan/Developments/Projects/research-devs/Blog/", "login")
