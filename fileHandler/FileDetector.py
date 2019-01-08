# --the code at this file will detect files which contains a corresponding substring at the file name
import os
import re


class FileDetector:
    # --method to detect the files
    # --root is the path of the source files and the anchor_str is the corresponding substring to be found in the file
    # --names
    def detect_files(self, root):
        # sourceList = open("sourceList.txt", "w")
        file_paths = []
        for paths, sub_dirs, files in os.walk(root):
            for file_path in files:
                base_name = os.path.basename(file_path)
                file_name = os.path.splitext(base_name)
                if file_name[1] == ".php" or file_name[1] == ".html":
                    full_path = os.path.join(paths, file_path)
                    file_paths.append(full_path)
                    # sourceList.write(full_path + "\n")
        return file_paths
        # sourceList.close()

    # --in order get the service from this function, the table name that contains the users must be known
    # --this function will detect the files which are connected with the login
    def detect_access_files(self, file_list, user_table_name):
        for file in file_list:
            with open(file, "r") as source_file:
                orig = source_file.read()
            source = orig.replace("\n", " ")

            # --these conditions will select the files which are connected to the table that contains the user data
            if re.findall("select(.*?)" + user_table_name, source).__len__() > 0:
                print("select ===> " + file)
                connected_files = self.detect_connected_files(file_list, self.get_file_name(file))
                self.print_list(connected_files)
            if re.findall("insert(.*?)" + user_table_name, source).__len__() > 0:
                print("insert ===> " + file)
                connected_files = self.detect_connected_files(file_list, self.get_file_name(file))
                self.print_list(connected_files)
            if re.findall("update(.*?)" + user_table_name, source).__len__() > 0:
                print("update ===> " + file)
                connected_files = self.detect_connected_files(file_list, self.get_file_name(file))
                self.print_list(connected_files)
            if re.findall("delete(.*?)" + user_table_name, source).__len__() > 0:
                print("delete ===> " + file)
                connected_files = self.detect_connected_files(file_list, self.get_file_name(file))
                self.print_list(connected_files)

            # --not yet completed

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

