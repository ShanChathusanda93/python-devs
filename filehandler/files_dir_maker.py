import os
import datetime
import re

from bs4 import BeautifulSoup

from dataobjects.detail_keeper_do import DetailsKeeperDO
from filehandler.connection_creator import ConnectionCreator
from stringfinder.reference_finder import ReferenceFinder
from stringfinder.source_replacer import SourceReplacer
from stringfinder.include_tree_detector import incl_tree
from dbaccess.components_register import ComponentRegistry


class FilesDirectoryMaker:
    def create_target_directory(self, directory_path):
        access_rights = 0o755
        if not os.path.exists(directory_path):
            os.mkdir(directory_path, access_rights)

    # -- in the future work in this method, try to identify the aql queries and the database connection file and then \
    #    convert these into the joomla format
    def create_target_file(self, target_directory_path, source_file_path):
        target_content = ""
        target_file_path = ""
        source_replacer = SourceReplacer()
        self.create_target_directory(target_directory_path)
        avoided_file_list = DetailsKeeperDO.get_avoided_file_list(DetailsKeeperDO)
        if DetailsKeeperDO.get_db_conn_file(DetailsKeeperDO) == source_file_path:
            conn_creator = ConnectionCreator()
            target_content = conn_creator.get_new_database_access_file()
            target_file_path = target_directory_path + "/" + "connection.php"
        elif source_file_path not in avoided_file_list:
            base_name = os.path.basename(source_file_path)
            with open(source_file_path, "r") as source_file:
                source_code = source_file.read().replace("\n", " ")
            target_file_path = target_directory_path + "/" + base_name
            # --check whether the files contain sql queries and convert them to joomla format
            source_code = source_replacer.replace_session_start(source_code)
            source_code = source_replacer.replace_session_details_assignment(source_code)
            source_code = source_replacer.replace_session_details_extraction(source_code)
            source_code = source_replacer.replace_media_references(source_code, source_file_path,
                                                                   DetailsKeeperDO.get_source_dir_path(DetailsKeeperDO))
            source_code = BeautifulSoup(source_code, "html.parser")
            target_content = source_code.prettify()
        if target_file_path != "":
            if not os.path.exists(target_file_path):
                with open(target_file_path, "w") as helper_file:
                    helper_file.write(target_content)

    def create_target_parent_file(self, target_directory_path, source_file_path):
        reference_finder = ReferenceFinder()
        source_replacer = SourceReplacer()
        base_name = os.path.basename(source_file_path)
        with open(source_file_path) as source_file:
            source_code = source_file.read().replace("\n", " ")
        php_occurrences = reference_finder.get_php_occurrences(source_code)
        includes = reference_finder.get_included_php_file_paths(php_occurrences, source_dir_path="",
                                                                need_compl_path=False)
        requires = reference_finder.get_required_php_file_paths(php_occurrences, source_dir_path="",
                                                                need_compl_path=False)
        if includes.__len__() > 0:
            source_code = source_replacer.replace_includes(source_code, includes)
        if requires.__len__() > 0:
            source_code = source_replacer.replace_requires(source_code, requires)

        source_code = source_replacer.replace_session_start(source_code)
        source_code = source_replacer.replace_session_details_assignment(source_code)
        source_code = source_replacer.replace_session_details_extraction(source_code)
        source_code = source_replacer.replace_media_references(source_code, source_file_path,
                                                               DetailsKeeperDO.get_source_dir_path(DetailsKeeperDO))

        source_code = BeautifulSoup(source_code, "html.parser")
        source_code = source_code.prettify()
        target_file_path = target_directory_path + "/" + base_name
        if not os.path.exists(target_file_path):
            with open(target_file_path, "w+") as helper_file:
                helper_file.write(source_code)

    def create_main_module_file(self, source_file_path):
        reference_finder = ReferenceFinder()
        source_replacer = SourceReplacer()
        component_register = ComponentRegistry()
        base_name = os.path.basename(source_file_path)
        file_name_details = os.path.splitext(base_name)
        target_dir_path = "/opt/lampp/htdocs/JoomlaResearchTest/modules/mod_" + file_name_details[0].lower()
        main_module_file_path = target_dir_path + "/mod_" + base_name.lower()
        with open(source_file_path, "r") as source_file:
            source_code = source_file.read().replace("\n", " ")
        php_occurrences = reference_finder.get_php_occurrences(source_code)
        complete_includes = []
        complete_includes.extend(reference_finder.get_included_php_file_paths(php_occurrences,
                                                                              DetailsKeeperDO.get_source_dir_path(
                                                                                  DetailsKeeperDO),
                                                                              need_compl_path=True))
        includes = []
        includes.extend(reference_finder.get_included_php_file_paths(php_occurrences,
                                                                     DetailsKeeperDO.get_source_dir_path(
                                                                         DetailsKeeperDO), need_compl_path=False))
        complete_requires = []
        complete_requires.extend(reference_finder.get_required_php_file_paths(php_occurrences,
                                                                              DetailsKeeperDO.get_source_dir_path(
                                                                                  DetailsKeeperDO),
                                                                              need_compl_path=True))
        requires = []
        requires.extend(reference_finder.get_required_php_file_paths(php_occurrences,
                                                                     DetailsKeeperDO.get_source_dir_path(
                                                                         DetailsKeeperDO), need_compl_path=False))

        if complete_includes.__len__() > 0:
            for incl_file in complete_includes:
                incl_tree(incl_file, target_dir_path)
            source_code = source_replacer.replace_includes(source_code, includes)
        source_code = source_replacer.replace_session_management(source_code)
        source_code = source_replacer.replace_media_references(source_code, source_file_path,
                                                               DetailsKeeperDO.get_source_dir_path(DetailsKeeperDO))
        main_module_file_header = "<?php\n" \
                                  "/***\n" \
                                  "*@package Joomla.Site\n" \
                                  "*@subpackage mod_" + file_name_details[0] + "\n" \
                                  "*@license GNU/GPL, see LICENSE.php\n" \
                                  "@copyright Copyright (C) 2005 - 2018, Open Source Matters, Inc. All rights " \
                                  "reserved.\n" \
                                  "***/\n" \
                                  "// no direct access\n" \
                                  "defined('_JEXEC') or die;" \
                                  "?>"
        source_code = main_module_file_header + source_code
        source_code = BeautifulSoup(source_code, "html.parser")
        with open(main_module_file_path, "w+") as module_file:
            module_file.write(source_code.prettify())
        self.create_target_directory(target_dir_path + "/language")
        self.create_target_directory(target_dir_path + "/language/en-GB")
        self.create_target_directory(target_dir_path + "/tmpl")
        self.create_module_xml_file(target_dir_path)
        title = component_register.register_module("mod_" + file_name_details[0].replace(" ", "_").lower())
        return title

    def create_module_xml_file(self, target_dir_path):
        module_file = ""
        helpers = []
        current_time = datetime.datetime.now()
        date_string = str(current_time.month) + " " + str(current_time.year)
        file_name_string = ""
        for root, dirs, files in os.walk(target_dir_path):
            for file in files:
                if "mod" in file:
                    module_file = file
                else:
                    helpers.append(file)
                    file_name_string = file_name_string + "<filename>" + file + "</filename>\n"
        module_det = module_file.split(".")
        target_xml_string = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n" \
                            "<extension type=\"module\" version=\"3.1\" client=\"site\" method=\"upgrade\">\n\t" \
                            "<name>" + module_det[0] + "</name>\n" \
                            "<author>Joomla! Research Project</author>\n" \
                            "<creationDate>" + date_string + "</creationDate>\n" \
                            "<copyright>Copyright (C) 2005 - 2018 Open Source Matters. All rights " \
                            "reserved.</copyright>\n" \
                            "<license>GNU General Public License version 2 or later; see LICENSE.txt</license>\n" \
                            "<authorEmail>authoremail@gmail.com</authorEmail>\n" \
                            "<authorUrl>www.authorurl.com</authorUrl>\n" \
                            "<version>1.1.0</version>\n" \
                            "<description>" + module_det[0] + " module</description>\n" \
                            "<!-- This section defined which files and folders will be part of this module -->\n" \
                            "<files>\n\t" \
                            "<filename module=\"" + module_det[0] + "\">" + module_file + "</filename>\n" \
                            "<folder>tmpl</folder>\n" + file_name_string + "</files>\n" \
                            "<languages>\n" \
                            "<language tag=\"en_GB\">en_GB.mod_my_first_form.ini</language>\n" \
                            "<language tag=\"en_GB\">en_GB.mod_my_first_form.sys.ini</language>\n" \
                            "</languages>\n" \
                            "<config>\n" \
                            "<fields name=\"params\">\n" \
                            "<fieldset name=\"basic\">\n" \
                            "<field name=\"parent\" type=\"category\" extension=\"com_content\" published=\"\" " \
                            "label=\"" + module_det[0] + " Label\" description=\"" + module_det[0] + " module\"/>\n" \
                            "</fieldset>\n" \
                            "</fields>\n" \
                            "</config>\n" \
                            "</extension>\n"
        target_file_path = target_dir_path + "/" + module_det[0] + ".xml"
        target_xml_string = BeautifulSoup(target_xml_string, "xml")
        with open(target_file_path, "w+") as module_xml_file:
            module_xml_file.write(target_xml_string.prettify())

    def replace_main_file_includes(self, source_code):
        reference_finder = ReferenceFinder()
        php_occurrences = reference_finder.get_php_occurrences(source_code)
        complete_includes = reference_finder.get_included_php_file_paths(php_occurrences,
                                                                         DetailsKeeperDO.get_source_dir_path(
                                                                             DetailsKeeperDO), True)
        includes = reference_finder.get_included_php_file_paths(php_occurrences, DetailsKeeperDO.get_source_dir_path(
            DetailsKeeperDO), False)
        i = 0
        for complete_include in complete_includes:
            module_title = self.create_main_module_file(complete_include)
            replace_string = "?> {module " + module_title + "} <?php"
            source_code = re.sub(r"include(\s*)(\"|\')" + re.escape(includes[i]) + r"(\"|\')(\s*);",
                                 replace_string, source_code)
        return source_code


file_maker = FilesDirectoryMaker()
# DetailsKeeperDO.set_source_dir_path(DetailsKeeperDO, "/opt/lampp/htdocs/Blog")
# file_maker.create_main_module_file("/opt/lampp/htdocs/Blog/TreeTest/a.php")

with open("/opt/lampp/htdocs/Blog/Login System/login_phpcode.php", "r") as file:
    source = file.read().replace("\n", " ")
DetailsKeeperDO.set_source_dir_path(DetailsKeeperDO, "/opt/lampp/htdocs/Blog")
source = source.replace("require_once", "include")
source = source.replace("require", "include")
source = file_maker.replace_main_file_includes(source)
print(source)

