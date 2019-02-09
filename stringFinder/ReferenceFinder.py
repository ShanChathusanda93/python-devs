# --this class is implemented to detect the include, require and require_once functions in php files
import os
import re


class ReferenceFinder:
    # --path of the source web application directory
    baseSourcePath = ""

    # --main method that detect the includes, required and require_once files
    def references_detector(self, file_list, avoided_files, base_code_path):
        # --setting a value to a global variable
        global baseSourcePath
        baseSourcePath = base_code_path

        # --list of files that are referenced as includes
        includes_list = open(
            "/home/shan/Developments/Projects/research-devs/python-devs/stringFinder/created_files/includeFileList.txt",
            "a")

        # --list of files that are referenced as required and require_once
        # required_list = open("/home/shan/Developments/Projects/research-devs/python-devs/stringFinder/created_files"
        #                      "/requiredFileList.txt", "a")
        all_included_files = []
        all_required_files = []
        for file in file_list:
            with open(file, "r") as source_file:
                source_code = source_file.read().replace("\n", " ")
                source_dir_path = os.path.dirname(file)
            php_occurrences = self.php_detector(source_code)
            complete_includes = self.include_detector(php_occurrences, source_dir_path, True)
            complete_requires = self.require_detector(php_occurrences, source_dir_path, True)

            if complete_includes.__len__() != 0:
                for include in complete_includes:
                    if os.path.exists(include):
                        if not any(include in include_file for include_file in avoided_files):
                            if not any(include in include_file for include_file in all_included_files):
                                all_included_files.append(include)

            if complete_requires.__len__() != 0:
                for requires in complete_requires:
                    if os.path.exists(requires):
                        if not any(requires in require_file for require_file in avoided_files):
                            if not any(requires in require_file for require_file in all_required_files):
                                all_required_files.append(requires)

        for i in all_included_files:
            includes_list.write(i + "\n")
        for r in all_required_files:
            includes_list.write(r + "\n")
        includes_list.close()
        # required_list.close()

    # --detect php code snippets from the provided source code and returns the php occurrences
    def php_detector(self, source_code):
        occurrences = re.findall('<\?php(.*?)\?>', source_code)
        return occurrences

    # --detect include files from the provided php occurrences and returns the include file path list
    def include_detector(self, php_occurrences, source_dir_path, need_compl_path):
        complete_includes = []
        for occurrence in php_occurrences:
            includes = re.findall('include \'(.*?)\';', occurrence)
            if need_compl_path:
                if includes.__len__() != 0:
                    complete_includes.append(self.path_completer(includes, source_dir_path))
            else:
                if includes.__len__() != 0:
                    for incl in includes:
                        complete_includes.append(incl)
        return complete_includes

    # --detect require_once and require files from the provided php occurrences and returns the file path list
    def require_detector(self, php_occurrences, source_dir_path, need_compl_path):
        complete_requires = []
        for occurrence in php_occurrences:
            require_once = re.findall('require_once \'(.*?)\';', occurrence)
            if need_compl_path:
                if require_once.__len__() != 0:
                    complete_requires.append(self.path_completer(require_once, source_dir_path))
            else:
                for r in require_once:
                    complete_requires.append(r)

            requires = re.findall("require \'(.*?)\';", occurrence)
            if need_compl_path:
                if requires.__len__() != 0:
                    complete_requires.append(self.path_completer(requires, source_dir_path))
            else:
                for r in requires:
                    complete_requires.append(r)

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
        for file_path in file_path_list:
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
