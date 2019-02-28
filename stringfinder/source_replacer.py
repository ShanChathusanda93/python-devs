import os
import re

from filehandler.file_migrator import FileMigrator
from stringfinder.reference_finder import ReferenceFinder


class SourceReplacer:
    # def replace_source(included_files, database_connect_file, source, article_files):
    #     for included_file in included_files:
    #         if database_connect_file in included_file:
    #             db_connection = "/home/shan/Developments/Projects/research-devs/python-devs/filehandler" \
    #                             "/phpSnippets/dbconnection/connection.php"
    #             source = source.replace(included_file, db_connection)
    #         else:
    #             if any("/" + included_file in i for i in article_files):
    #                 file_name = os.path.splitext(included_file)
    #                 for occur in php_occurrences:
    #                     if included_file in occur:
    #                         occur_words = str(occur).split()
    #                         old = "<?php" + str(occur) + "?>"
    #                         replacement = "{article " + file_name[0] + "}\n[introtext]\n[fulltext]\n{/article}"
    #                         if occur_words.__len__() == 2:
    #                             source = source.replace(old, replacement)
    #                         else:
    #                             source = source.replace(occur, replacement)
    #             elif any("/" + included_file in j for j in separate_files):
    #                 for occur in php_occurrences:
    #                     if included_file in occur:
    #                         source = source.replace(occur, "include 'file_path_to/" + included_file + "';")

    def replace_media_references(self, source_code, source_file_path, main_source_dir_path):
        # this path should be an user input
        target_media_dir_path = "/opt/lampp/htdocs/JoomlaResearchTest/images/"
        reference_finder = ReferenceFinder()
        file_migrator = FileMigrator()
        media_references_file_paths = reference_finder.get_media_references(source_file_path, main_source_dir_path,
                                                                            need_full_path=True)
        if media_references_file_paths.__len__() > 0:
            for media_file in media_references_file_paths:
                file_migrator.move_media_files(media_file, target_media_dir_path)
        media_references = reference_finder.get_media_references(source_file_path, main_source_dir_path,
                                                                 need_full_path=False)
        for media_ref in media_references:
            file_name = os.path.basename(media_ref)
            source_code = source_code.replace(media_ref, "images/" + file_name)
        return source_code

    def replace_includes(self, source_code, includes):
        for incl in includes:
            base_name = os.path.basename(incl)
            source_code = re.sub(r"include(\s*)(\"|\')" + re.escape(incl) + r"(\"|\')(\s*);",
                                 "require_once dirname(__FILE__).'/" + base_name + "';\n", source_code)
        return source_code

    def replace_requires(self, source_code, requires):
        for req in requires:
            base_name = os.path.basename(req)
            source_code = re.sub(r"require(_once*|\s*)(\s*)(\"|\')" + re.escape(req) + "(\"|\')(\s*);",
                                 "require_once dirname(__FILE__).'/" + base_name + "';\n", source_code)
        return source_code

    def replace_session_management(self, source_code):
        source_code = self.replace_session_start(source_code)
        source_code = self.replace_session_details_assignment(source_code)
        source_code = self.replace_session_details_extraction(source_code)
        return source_code

    def replace_session_start(self, source_code):
        replace_string = "$session = JFactory::getSession();"
        source_code = re.sub(r"session_start\(\);", replace_string, source_code)
        return source_code

    def replace_session_details_assignment(self, source_code):
        reference_finder = ReferenceFinder()
        session_details = reference_finder.get_session_assignment_details(source_code)
        session_var_details = []
        session_var_details.extend(session_details[0])
        starts = []
        starts.extend(session_details[1])
        ends = []
        ends.extend(session_details[2])

        i = 0
        previous_src = source_code
        for session_var in session_var_details:
            replace_string = "$session -> set('" + session_var[1] + "', " + session_var[5] + ");\n"
            old_string = previous_src[starts[i]:ends[i]]
            source_code = source_code.replace(old_string, replace_string)
            i = i + 1
        # source_code = BeautifulSoup(source_code, "html.parser")
        # with open("/home/shan/Developments/Projects/research-devs/python-devs/filehandler/alteredSrc/fin.txt", "w+"
        #           ) as file:
        #     file.write(source_code.prettify())
        return source_code

    def replace_session_details_extraction(self, source_code):
        reference_finder = ReferenceFinder()
        session_details = reference_finder.get_session_extraction_details(source_code)
        session_var_details = []
        session_var_details.extend(session_details[0])
        starts = []
        starts.extend(session_details[1])
        ends = []
        ends.extend(session_details[2])
        previous_src = source_code
        i = 0
        for session_var in session_var_details:
            replace_string = "$session -> get('" + session_var[1] + "');"
            old_string = previous_src[starts[i]:ends[i]]
            source_code = source_code.replace(old_string, replace_string)
            i = i + 1
        # source_code = BeautifulSoup(source_code, "html.parser")
        # with open("/home/shan/Developments/Projects/research-devs/python-devs/filehandler/alteredSrc/fin.txt", "w+"
        #           ) as file:
        #     file.write(source_code.prettify())
        return source_code
