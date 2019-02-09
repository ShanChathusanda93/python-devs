import os

def replace_source(included_files, database_connect_file, source, article_files):
    for included_file in included_files:
        if database_connect_file in included_file:
            db_connection = "/home/shan/Developments/Projects/research-devs/python-devs/fileHandler" \
                            "/phpSnippets/dbconnection/connection.php"
            source = source.replace(included_file, db_connection)
        else:
            if any("/" + included_file in i for i in article_files):
                file_name = os.path.splitext(included_file)
                for occur in php_occurrences:
                    if included_file in occur:
                        occur_words = str(occur).split()
                        old = "<?php" + str(occur) + "?>"
                        replacement = "{article " + file_name[0] + "}\n[introtext]\n[fulltext]\n{/article}"
                        if occur_words.__len__() == 2:
                            source = source.replace(old, replacement)
                        else:
                            source = source.replace(occur, replacement)
            elif any("/" + included_file in j for j in separate_files):
                for occur in php_occurrences:
                    if included_file in occur:
                        source = source.replace(occur, "include 'file_path_to/" + included_file + "';")