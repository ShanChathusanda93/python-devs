import os
import re


# print("Hello World from python...!!!")
#
# for i in range(1, 10):
#     print(i)
#     print("\n")
from dataobjects.navigation_do import NavigationDO


def detect_files():
    file_paths = []
    for paths, sub_dirs, files in os.walk("/home/shan/Developments/Projects/research-devs/Blog"):
        for file_path in files:
            base_name = os.path.basename(file_path)
            file_name = os.path.splitext(base_name)
            if file_name[1] == ".php" or file_name[1] == ".html":
                full_path = os.path.join(paths, file_path)
                file_paths.append(full_path)
                # print(full_path)
    return file_paths


def get_navigation_files_details(file_list):
        navigation_files_details = []
        for file in file_list:
            with open(file, "r") as source_file:
                original_src = source_file.read().replace("\n", " ")
                original_src = original_src.replace("\t", " ")
            ul_lists = re.findall("<ul(.*?)<\/ul>", original_src)
            if ul_lists.__len__() > 0:
                navigations = []
                for ul_list in ul_lists:
                    navigators = re.findall("<li>(.*?)</li>", ul_list)
                    for nav in navigators:
                        navigations.append(nav)
                if navigations.__len__() > 0:
                    navigator = NavigationDO()
                    navigator.set_nav_file_name(file)
                    navigator.set_navigations(navigations)
                    navigation_files_details.append(navigator)
        return navigation_files_details


def get_hello_with_name(name_str):
    hello = "Hello Mr. " + name_str
    return hello
    # print(hello)


def square(value):
    return value * value


# get_source_file_paths()
