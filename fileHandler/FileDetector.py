# --the code at this file will detect files which contains a corresponding substring at the file name
import os
import re
from fileHandler.NavigationDO import NavigationDO


class FileDetector:
    # --method to detect the files
    # --root is the path of the source files and the anchor_str is the corresponding substring to be found in the file
    # --names
    def detect_files(self, root):
        file_paths = []
        for paths, sub_dirs, files in os.walk(root):
            for file_path in files:
                base_name = os.path.basename(file_path)
                file_name = os.path.splitext(base_name)
                if file_name[1] == ".php" or file_name[1] == ".html":
                    full_path = os.path.join(paths, file_path)
                    file_paths.append(full_path)
        return file_paths

    # --in order get the service from this function, the table name that contains the users must be known
    # --this function will detect the files which are connected with the login
    def detect_access_files(self, file_list, user_tables):
        access_files = []
        for file in file_list:
            with open(file, "r") as source_file:
                orig = source_file.read()
            source = orig.replace("\n", " ")

            # --this condition will detect the database connection file without duplicates
            if re.findall("mysqli_connect\(", source.lower()).__len__() > 0:
                if not any(file in a_file for a_file in access_files):
                    access_files.append(file)
            elif re.findall("mysql_connect\(", source.lower()).__len__() > 0:
                if not any(file in a_file for a_file in access_files):
                    access_files.append(file)

            # --these conditions will select the files which are connected to the table that contains the user data
            # --without duplicates
            for user_table in user_tables:
                if re.findall("select(.*?)" + user_table, source.lower()).__len__() > 0:
                    if not any(file in a_file for a_file in access_files):
                        access_files.append(file)
                    connected_files = self.detect_connected_files(file_list, self.get_file_name(file))
                    for c_file in connected_files:
                        if not any(c_file in a_file for a_file in access_files):
                            access_files.append(c_file)

                if re.findall("insert(.*?)" + user_table, source.lower()).__len__() > 0:
                    if not any(file in a_file for a_file in access_files):
                        access_files.append(file)
                    connected_files = self.detect_connected_files(file_list, self.get_file_name(file))
                    for c_file in connected_files:
                        if not any(c_file in a_file for a_file in access_files):
                            access_files.append(c_file)

                if re.findall("update(.*?)" + user_table, source.lower()).__len__() > 0:
                    if not any(file in a_file for a_file in access_files):
                        access_files.append(file)
                    connected_files = self.detect_connected_files(file_list, self.get_file_name(file))
                    for c_file in connected_files:
                        if not any(c_file in a_file for a_file in access_files):
                            access_files.append(c_file)

                if re.findall("delete(.*?)" + user_table, source.lower()).__len__() > 0:
                    if not any(file in a_file for a_file in access_files):
                        access_files.append(file)
                    connected_files = self.detect_connected_files(file_list, self.get_file_name(file))
                    for c_file in connected_files:
                        if not any(c_file in a_file for a_file in access_files):
                            access_files.append(c_file)

            # --this condition can detect the files which contains the input type as password without duplicates
            if re.findall("<input(.*?)password", source.lower()).__len__() > 0:
                if not any(file in a_file for a_file in access_files):
                    access_files.append(file)

            # --this condition can detect the logout files without duplicates
            if re.findall("session_destroy", source.lower()).__len__() > 0:
                if not any(file in a_file for a_file in access_files):
                    access_files.append(file)
        return access_files

    def get_database_connect_file_name(self, file_list):
        connection_file = []
        for file in file_list:
            with open(file, "r") as source_file:
                orig = source_file.read()
            source = orig.replace("\n", " ")
            # --this condition will detect the database connection file without duplicates
            if re.findall("mysqli_connect\(", source.lower()).__len__() > 0:
                connection_file.append(file)
            elif re.findall("mysql_connect\(", source.lower()).__len__() > 0:
                connection_file.append(file)
        return connection_file

    def get_content_files(self, file_list, access_file_list):
        content_files = []
        for file in file_list:
            if not any(file in files for files in access_file_list):
                content_files.append(file)
        return content_files

    def get_navigation_files_details(self, file_list):
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
                    navigation_files_details.append(NavigationDO(file, navigations))
        return navigation_files_details

    def get_file_name(self, file):
        base = os.path.basename(file)
        file_details = os.path.splitext(base)
        file_name = file_details[0] + file_details[1]
        return file_name

    def detect_connected_files(self, file_list, file_to_be_searched):
        connected_file_list = []
        for file in file_list:
            with open(file, "r") as source_file:
                orig = source_file.read()
            source = orig.replace("\n", " ")
            if re.findall(file_to_be_searched, source).__len__() > 0:
                connected_file_list.append(file)
        return connected_file_list

    def print_list(self, list):
        for l in list:
            print(l)

