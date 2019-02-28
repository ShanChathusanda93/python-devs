import os
import re

from dataobjects.navigation_do import NavigationDO


class Test:
    def square(self, value):
        return value * value

    def set_data_objects(self, name):
        navigator = NavigationDO()
        navigator.set_nav_file_name("File Name is : " + name)
        return navigator

    def get_navigation_files_details(self, file_list):
        navigation_files_details = []
        for file in file_list:
            with open(file, "r") as source_file:
                original_src = source_file.read().replace("\n", " ")
                original_src = original_src.replace("\t", " ")
            ul_lists = re.findall("<ul(.*?)<\/ul>", original_src)
            if ul_lists.__len__() > 0:
                navigation_details = []
                for ul_list in ul_lists:
                    navigators = re.findall("<li>(.*?)</li>", ul_list)
                    for nav in navigators:
                        navigation_details.append(nav)
                if navigation_details.__len__() > 0:
                    navigator = NavigationDO()
                    navigator.set_nav_file_name(file)
                    navigator.set_navigations(navigation_details)
                    navigation_files_details.append(navigator)
        return navigation_files_details


def square_without_class(value):
    if os.path.exists("value") == False:
        return value * value
