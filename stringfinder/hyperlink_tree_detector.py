import os

from dataobjects.detail_keeper_do import DetailsKeeperDO
from filehandler.files_dir_maker import FilesDirectoryMaker
from filehandler.source_reader import SourceReader
from stringfinder.reference_finder import ReferenceFinder
from stringfinder.source_replacer import SourceReplacer
from dbaccess.components_register import ComponentRegistry
from dbaccess.component_retriever import ComponentRetriever

article_creation_tree = dict()
file_tree = dict()
created_article_details = dict()


def create_nested_hyperlinked_articles(file_path):
    global article_creation_tree
    global file_tree
    global created_article_details

    reference_finder = ReferenceFinder()

    avoided_file_list = DetailsKeeperDO.get_avoided_file_list(DetailsKeeperDO)
    source_code = SourceReader.get_source(file_path)
    hyperlink_details = reference_finder.get_links_details(source_code)
    if hyperlink_details.__len__() > 0:
        for link_details in hyperlink_details:
            # print(link_details)
            if not "No File" in link_details[1]:
                if any(link_details[1] in avoided_file for avoided_file in avoided_file_list):
                    # print("avoided file")
                    pass
                else:
                    # print("not avoided file. File sent to create an article.")
                    linked_source_code = SourceReader.get_source(link_details[1])
                    child_hyperlinks = reference_finder.get_links_details(linked_source_code)
                    if child_hyperlinks.__len__() > 0:
                        file_tree.update({link_details[1]: file_path})
                        create_nested_hyperlinked_articles(link_details[1])
                    else:
                        file_tree.update({link_details[1]: file_path})
                        create_child_articles(link_details[1])
                        if file_path in article_creation_tree:
                            count = article_creation_tree[file_path]
                            count = count + 1
                            article_creation_tree.update({file_path: count})
                        else:
                            count = 1
                            article_creation_tree.update({file_path: count})
                    parent_file = file_tree[link_details[1]]
                    parent_article_count = article_creation_tree[parent_file]
                    if parent_article_count == hyperlink_details.__len__():
                        create_parent_article_file(parent_file)
                        if parent_file != check_root():
                            elder_file = file_tree[parent_file]
                            if elder_file in article_creation_tree:
                                elder_count = article_creation_tree[elder_file]
                                elder_count = elder_count + 1
                                article_creation_tree.update({elder_file: elder_count})
                            else:
                                elder_count = 1
                                article_creation_tree.update({elder_file: elder_count})
            else:
                # print("External file is referenced.")
                file_tree.update({link_details[1]: file_path})
                if file_path in article_creation_tree:
                    count = article_creation_tree[file_path]
                    count = count + 1
                    article_creation_tree.update({file_path: count})
                else:
                    count = 1
                    article_creation_tree.update({file_path: count})

                # old_link = "<a" + link_details[2] + "/a>"
                # replacement_link = "<p><a href=\"" + link_details[0][3] + "\" target=\"_blank\" " \
                #                                                           "rel=\"noopener noreferrer\">" + \
                #                    link_details[0][6] + "</a></p>"
                # source_code = source_code.replace(old_link, replacement_link, source_code)


def create_child_articles(file_path):
    source_replacer = SourceReplacer()
    reference_finder = ReferenceFinder()
    file_maker = FilesDirectoryMaker()
    article_register = ComponentRegistry()

    source_code = SourceReader.get_source(file_path)
    source_code = source_replacer.replace_styles(source_code)
    source_code = source_replacer.replace_session_management(source_code)
    source_code = source_replacer.replace_media_references(source_code, file_path, "/opt/lampp/htdocs/Blog")
    include_counter = reference_finder.has_include(file_path)
    if include_counter == 1:
        source_code = file_maker.replace_main_file_includes(source_code)
    # --send to database
    base_name = os.path.basename(file_path)
    file_name = os.path.splitext(base_name)
    article_register.register_article(source_code, file_name[0])
    # print("linked article created : " + file_path)
    # pass


def check_root():
    values = []
    for key, val in file_tree.items():
        values.append(val)
    return values[0]


def print_tree():
    for key, val in article_creation_tree.items():
        print(key + " => " + str(val))


def create_parent_article_file(file_path):
    source_replacer = SourceReplacer()
    reference_finder = ReferenceFinder()
    file_maker = FilesDirectoryMaker()
    article_register = ComponentRegistry()
    component_retriever = ComponentRetriever()

    source_code = SourceReader.get_source(file_path)
    hyperlink_details = reference_finder.get_links_details(source_code)
    avoided_file_list = DetailsKeeperDO.get_avoided_file_list(DetailsKeeperDO)
    for link_details in hyperlink_details:
        if not "No File" in link_details[1]:
            if not any(link_details[1] in avoided_file for avoided_file in avoided_file_list):
                base_name = os.path.basename(link_details[1])
                file_name = os.path.splitext(base_name)
                link_string = link_details[2].split(">")
                article_id = component_retriever.get_article_id("Article " + file_name[0])
                new_link_str = ' href="index.php?option=com_content&amp;view=article&amp;id=' + str(article_id) + ">" + \
                               link_string[1]
                source_code = source_code.replace(link_details[2], new_link_str)
            # print(link_details[2])
    source_code = source_replacer.replace_session_management(source_code)
    source_code = source_replacer.replace_media_references(source_code, file_path, "/opt/lampp/htdocs/Blog")
    include_counter = reference_finder.has_include(file_path)
    if include_counter == 1:
        source_code = file_maker.replace_main_file_includes(source_code)
    article_base_name = os.path.basename(file_path)
    article_name = os.path.splitext(article_base_name)
    article_register.register_article(source_code, article_name[0])
    # print("parent article created : " + file_path)


create_nested_hyperlinked_articles("/opt/lampp/htdocs/Blog/TreeTest/a.php")
# print_tree()
