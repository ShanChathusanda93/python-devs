import os

from bs4 import BeautifulSoup

from dataobjects.detail_keeper_do import DetailsKeeperDO
from filehandler.connection_creator import ConnectionCreator
from stringfinder.reference_finder import ReferenceFinder
from stringfinder.source_replacer import SourceReplacer

file_tree = dict()
file_creation_map = dict()


def incl_tree(file_name, target_dir_path):
    global file_tree
    global file_creation_map

    reference_finder = ReferenceFinder()
    with open(file_name) as source_file:
        source = source_file.read()
    source = source.replace("\n", " ")
    php = reference_finder.get_php_occurrences(source)
    if php.__len__() != 0:
        includes = reference_finder.get_included_php_file_paths(php, DetailsKeeperDO.
                                                                get_source_dir_path(DetailsKeeperDO),
                                                                need_compl_path=True)
        if includes.__len__() != 0:
            for include_file in includes:
                if os.path.exists(str(include_file)):
                    incl_counter = reference_finder.has_include(include_file)
                    if incl_counter == 1:
                        file_tree.update({include_file: file_name})
                        incl_tree(include_file, target_dir_path)
                    else:
                        file_tree.update({include_file: file_name})
                        # print("file created : " + include_file)
                        create_target_file(target_dir_path, include_file)
                        if file_name in file_creation_map:
                            count = file_creation_map[file_name]
                            count = count + 1
                            file_creation_map.update({file_name: count})
                        else:
                            count = 1
                            file_creation_map.update({file_name: count})
                    senior_file = file_tree[include_file]
                    senior_count = file_creation_map[senior_file]
                    if senior_count == includes.__len__():
                        # print("file created : " + senior_file)
                        create_target_parent_file(target_dir_path, senior_file)
                        if senior_file != check_root():
                            supreme_file = file_tree[senior_file]
                            if supreme_file in file_creation_map:
                                supreme_count = file_creation_map[supreme_file]
                                supreme_count = supreme_count + 1
                                file_creation_map.update({supreme_file: supreme_count})
                            else:
                                supreme_count = 1
                                file_creation_map.update({supreme_file: supreme_count})


def create_target_directory(directory_path):
    access_rights = 0o755
    if not os.path.exists(directory_path):
        os.mkdir(directory_path, access_rights)


def create_target_file(target_directory_path, source_file_path):
    target_content = ""
    target_file_path = ""
    source_replacer = SourceReplacer()
    create_target_directory(target_directory_path)
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


def create_target_parent_file(target_directory_path, source_file_path):
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


def print_tree():
    for key, val in file_creation_map.items():
        print(key + " => " + str(val))


def check_root():
    values = []
    for key, val in file_tree.items():
        values.append(val)
    return values[0]
