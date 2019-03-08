# --this class is implemented to detect the include, require and require_once functions in php files
import os
import re

from dataobjects.detail_keeper_do import DetailsKeeperDO
from filehandler.file_detector import FileDetector


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
            "/home/shan/Developments/Projects/research-devs/python-devs/stringfinder/created_files/includeFileList.txt",
            "a")

        # --list of files that are referenced as required and require_once
        # required_list = open("/home/shan/Developments/Projects/research-devs/python-devs/stringfinder/created_files"
        #                      "/requiredFileList.txt", "a")
        all_included_files = []
        all_required_files = []
        for file in file_list:
            with open(file, "r") as source_file:
                source_code = source_file.read().replace("\n", " ")
                source_dir_path = os.path.dirname(file)
            php_occurrences = self.get_php_occurrences(source_code)
            complete_includes = self.get_included_php_file_paths(php_occurrences, source_dir_path, True)
            complete_requires = self.get_required_php_file_paths(php_occurrences, source_dir_path, True)

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
    def get_php_occurrences(self, source_code):
        occurrences = re.findall('<\?php(.*?)\?>', source_code)
        return occurrences

    # --detect include files from the provided php occurrences and returns the include file path list
    def get_included_php_file_paths(self, php_occurrences, source_dir_path, need_compl_path):
        file_detector = FileDetector()
        file_list = file_detector.get_source_file_paths(source_dir_path)
        complete_includes = []
        for occurrence in php_occurrences:
            includes = re.findall(r'include (\'|\")(.*?)(\"|\');', occurrence)
            if need_compl_path:
                if includes.__len__() != 0:
                    for include_file in includes:
                        complete_includes.append(self.get_complete_path(str(include_file[1]), file_list))
            else:
                if includes.__len__() != 0:
                    for incl in includes:
                        complete_includes.append(str(incl[1]))
        return complete_includes

    # --detect require_once and require files from the provided php occurrences and returns the file path list
    def get_required_php_file_paths(self, php_occurrences, source_dir_path, need_compl_path):
        file_detector = FileDetector()
        file_list = file_detector.get_source_file_paths(source_dir_path)
        complete_requires = []
        for occurrence in php_occurrences:
            require_once = re.findall(r'require_once [\'|\"](.*?)[\"|\'];', occurrence)
            if need_compl_path:
                if require_once.__len__() != 0:
                    complete_requires.append(self.get_complete_path(str(require_once[1]), file_list))
            else:
                for r in require_once:
                    complete_requires.append(r)

            requires = re.findall(r"require [\'|\"](.*?)[\"|\'];", occurrence)
            if need_compl_path:
                if requires.__len__() != 0:
                    complete_requires.append(self.get_complete_path(str(requires[1]), file_list))
            else:
                for r in requires:
                    complete_requires.append(r)

        return complete_requires

    # --complete the paths from the relative paths to original paths and returns the file paths
    def get_complete_path(self, file_path, file_list):
        if "../../" in file_path:
            file_path = file_path.replace('../..', "")
        elif "../" in file_path:
            file_path = file_path.replace('..', "")
        matching = [file for file in file_list if file_path in file]
        if matching.__len__() > 0:
            for match in matching:
                return match
        else:
            return "No File"

    def has_include(self, file_path):
        # no_includes_files = []
        # has_includes_files = []
        # return_values = []
        include_counter = 0
        source_path = "/opt/lampp/htdocs/Blog"
        # for file_path in file_path_list:
        with open(file_path, "r") as source_file:
            source_code = source_file.read().replace("\n", " ")
        php_occurrences = self.get_php_occurrences(source_code)
        includes_occurrences = self.get_included_php_file_paths(php_occurrences, source_path, need_compl_path=False)
        require_occurrences = self.get_required_php_file_paths(php_occurrences, source_path, need_compl_path=False)

        if includes_occurrences.__len__() == 0 and require_occurrences.__len__() == 0:
            # no_includes_files.append(file_path)
            include_counter = 0
        else:
            # has_includes_files.append(file_path)
            include_counter = 1

        # return_values.append(no_includes_files)
        # return_values.append(has_includes_files)
        # return return_values
        return include_counter

    def get_media_references(self, file_name, source_path, need_full_path):
        file_detector = FileDetector()
        media_reference_paths = []
        media_files = file_detector.get_media_file_paths(source_path)
        with open(file_name, "r") as source_file:
            source = source_file.read().replace("\n", " ")
        image_references = re.findall("<img(.*?)src=\"(.*?)\"", source)
        if need_full_path:
            for img_ref in image_references:
                media_reference_paths.append(self.get_complete_path(str(img_ref[1]), media_files))
        else:
            for img_ref in image_references:
                media_reference_paths.append(str(img_ref[1]))
        return media_reference_paths

    def get_session_assignment_details(self, source_code):
        details = re.findall('\$_SESSION\[(\'|\")(.*?)(\"|\')\](\s*)=(\s*)(.*?);', source_code)
        starts = [m.start(0) for m in re.finditer('\$_SESSION(\[(\'|\")(.*?)(\"|\')\](\s*))=(\s*)(.*?);', source_code)]
        ends = [n.end(0) for n in re.finditer('\$_SESSION(\[(\'|\")(.*?)(\"|\')\](\s*))=(\s*)(.*?);', source_code)]
        session_details = [details, starts, ends]
        return session_details

    def get_session_extraction_details(self, source_code):
        details = re.findall("\$_SESSION\[(\'|\")(.*?)(\"|\')\]", source_code)
        starts = [m.start(0) for m in re.finditer('\$_SESSION\[(\'|\")(.*?)(\"|\')\]', source_code)]
        ends = [n.end(0) for n in re.finditer('\$_SESSION\[(\'|\")(.*?)(\"|\')\]', source_code)]
        session_details = [details, starts, ends]
        return session_details

    def get_links_details(self, source_code):
        details = []
        file_detector = FileDetector()
        file_list = file_detector.get_source_file_paths("/opt/lampp/htdocs/Blog")
        links_details = re.findall("<a(.*?)/a>", source_code)
        for link in links_details:
            link_details = []
            det = re.findall(r"href(\s*)=(\s*)(\"|\')(.*?)(\'|\")(\s*)>(.*?)<", link)
            complete_path = self.get_complete_path(det[0][3], file_list)
            link_details.append(det[0])
            link_details.append(complete_path)
            link_details.append(link)
            details.append(link_details)
        return details


# ref_finder = ReferenceFinder()
# DetailsKeeperDO.set_avoided_file_list(DetailsKeeperDO, ["/opt/lampp/htdocs/Blog/post views/view_posttext.php"])
# with open("/opt/lampp/htdocs/Blog/post views/view.php", "r") as file:
#     source = file.read().replace("\n", " ")
# source = re.sub(r"<!--(.*?)-->", " ", source)
# ref_finder.get_links_details(source)
