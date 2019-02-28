# --the code at this file will detect files which contains a corresponding substring at the file name
import os
import re

from dataobjects.navigation_do import NavigationDO
from dataobjects.detail_keeper_do import DetailsKeeperDO
from utils.Stack import Stack


class FileDetector:
    # --method to detect the files
    # --root is the path of the source files and the anchor_str is the corresponding substring to be found in the file
    # --names
    def get_source_file_paths(self, root):
        file_paths = []
        for paths, sub_dirs, files in os.walk(root):
            for file_path in files:
                base_name = os.path.basename(file_path)
                file_name = os.path.splitext(base_name)
                if file_name[1] == ".php" or file_name[1] == ".html":
                    full_path = os.path.join(paths, file_path)
                    file_paths.append(full_path)
        DetailsKeeperDO.source_dir_path = root
        DetailsKeeperDO.source_file_list = file_paths
        return file_paths

    def get_media_file_paths(self, root):
        media_file_paths = []
        for paths, sub_dirs, files in os.walk(root):
            for file_path in files:
                base_name = os.path.basename(file_path)
                media_file_name = os.path.splitext(base_name)
                if media_file_name[1] == ".jpg" or media_file_name[1] == ".png":
                    full_media_path = os.path.join(paths, file_path)
                    media_file_paths.append(full_media_path)
        return media_file_paths

    # --in order get the service from this function, the table name that contains the users must be known
    # --this function will detect the files which are connected with the login
    def get_user_management_file_paths(self, file_list, user_tables):
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
        indices = []
        ul_stack = Stack()
        navigation_files_details = []
        for file in file_list:
            with open(file, "r") as source_file:
                original_src = source_file.read().replace("\n", " ")
                original_src = original_src.replace("\t", "")
            ul_start_indices = [w.start(0) for w in re.finditer("<ul", original_src)]
            ul_end_indices = [e.end(0) for e in re.finditer("</ul>", original_src)]
            for ul_s_index in ul_start_indices:
                indices.append(ul_s_index)
            for ul_e_index in ul_end_indices:
                indices.append(ul_e_index)

            ul_segments = []
            if indices.__len__() > 0:
                indices.sort(reverse=False)
                for idx in indices:
                    if idx in ul_start_indices:
                        ul_stack.push(idx)
                    elif idx in ul_end_indices:
                        if ul_stack.size() == 1:
                            ul_start = ul_stack.pop()
                            ul_segments.append(original_src[ul_start:idx])
                        else:
                            ul_stack.pop()

            # ul_lists = re.findall("<ul(.*?)<\/ul>", original_src)
            if ul_segments.__len__() > 0:
                navigation_details = []
                for ul_segment in ul_segments:
                    navigators = re.findall("<li>(.*?)</li>", ul_segment)
                    for nav in navigators:
                        navigation_details.append(nav)
                if navigation_details.__len__() > 0:
                    navigator = NavigationDO()
                    navigator.set_nav_file_name(file)
                    navigator.set_navigations(navigation_details)
                    navigation_files_details.append(navigator)
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
