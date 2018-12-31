# --this class is implemented to detect the include, require and require_once functions in php files
import os
import re


class ReferenceFinder:
    # --base path of the source files
    baseSourcePath = "/home/shan/Developments/Projects/research-devs/Blog"

    # --main method that detect the includes, required and require_once files
    def reference_detector(self):
        # --open extracted source file path list
        with open("/home/shan/Developments/Projects/research-devs/python-devs/main/sourceList.txt",
                  "r") as source_files:
            file_list = source_files.read().splitlines()
            source_files.close()
        # --for testing purposes
        # file_list = ["/home/shan/Developments/Projects/research-devs/Blog/User/post/post_text_image_view.php",
        #              "/home/shan/Developments/Projects/research-devs/Blog/Frontend/frontend.php"]
        # file = "/home/shan/Developments/Projects/research-devs/Blog/User/post/post_text_image_view.php"

        # --list of file that are referenced as includes
        includes_list = open(
            "/home/shan/Developments/Projects/research-devs/python-devs/stringFinder/includeFileList.txt", "a")
        # --list of file that are referenced as required and require_once
        required_list = open("/home/shan/Developments/Projects/research-devs/python-devs/stringFinder/requiredFileList"
                             ".txt", "a")
        i = 0
        j = 0
        for file in file_list:
            with open(file, "r") as source_file:
                source_code = source_file.read().replace("\n", " ")
                source_dir_path = os.path.dirname(file)
            php_occurrences = self.php_detector(self, source_code)
            complete_includes = self.include_detector(self, php_occurrences, source_dir_path)
            complete_requires = self.require_detector(self, php_occurrences, source_dir_path)

            if complete_includes.__len__() != 0:
                i = i + 1
                # includes_list.write(str(i) + ". " + file + "\n")
                for include in complete_includes:
                    if os.path.exists(include):
                        includes_list.write(include + "\n")

            if complete_requires.__len__() != 0:
                j = j + 1
                # required_list.write(str(j) + ". " + file + "\n")
                for requires in complete_requires:
                    if os.path.exists(requires):
                        required_list.write(requires + "\n")
        includes_list.close()
        required_list.close()

    # --detect php code snippets from the provided source code and returns the php occurrences
    def php_detector(self, source_code):
        occurrences = re.findall('<\?php(.*?)\?>', source_code)
        return occurrences

    # --detect include files from the provided php occurrences and returns the include file path list
    def include_detector(self, php_occurrences, source_dir_path):
        complete_includes = []
        for occurrence in php_occurrences:
            includes = re.findall('include \'(.*?)\';', occurrence)
            if includes.__len__() != 0:
                complete_includes.append(self.path_completer(self, includes, source_dir_path))
        return complete_includes

    # --detect require_once and require files from the provided php occurrences and returns the file path list
    def require_detector(self, php_occurrences, source_dir_path):
        complete_requires = []
        for occurrence in php_occurrences:
            require_once = re.findall('require_once \'(.*?)\';', occurrence)
            if require_once.__len__() != 0:
                complete_requires.append(self.path_completer(self, require_once, source_dir_path))
            requires = re.findall("require \'(.*?)\';", occurrence)
            if requires.__len__() != 0:
                complete_requires.append(self.path_completer(self, requires, source_dir_path))
        return complete_requires

    # --complete the paths from the relative paths to original paths and returns the file paths
    def path_completer(self, file_paths, source_dir_path):
        for file_path in file_paths:
            if "../../" in file_path:
                return file_path.replace('../..', self.baseSourcePath)
            elif "../" in file_path:
                return file_path.replace('..', self.baseSourcePath)
            else:
                return source_dir_path + "/" + file_path

    def has_include(self, file_path_list):
        no_includes_files = []
        has_includes_files = []
        return_values = []
        source_path = "/home/shan/Developments/Projects/research-devs/Blog"
        # for file_path in file_path_list:
        file_path = "/home/shan/Developments/Projects/research-devs/Blog/User/user profile detail/edit_profile.php"
        file = open(file_path, "r")
        source_code = file.read()
        php_occurrences = self.php_detector(self, source_code)
        includes_occurrences = self.include_detector(self, php_occurrences, source_path)
        require_occurrences = self.require_detector(self, php_occurrences, source_path)

        if includes_occurrences.__len__() == 0 and require_occurrences.__len__() == 0:
            no_includes_files.append(file_path)
        else:
            has_includes_files.append(file_path)
        return_values.append(no_includes_files)
        return_values.append(has_includes_files)
        return return_values
