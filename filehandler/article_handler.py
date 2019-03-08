import os

from dbaccess.component_retriever import ComponentRetriever
from dbaccess.components_register import ComponentRegistry
from filehandler.files_dir_maker import FilesDirectoryMaker
from filehandler.source_reader import SourceReader
from stringfinder.reference_finder import ReferenceFinder
from stringfinder.source_replacer import SourceReplacer


class ArticleHandler:
    def create_article(self, source_file_path):
        reference_finder = ReferenceFinder()
        source_replacer = SourceReplacer()
        file_maker = FilesDirectoryMaker()
        article_register = ComponentRegistry()
        component_retriever = ComponentRetriever()

        article_base_name = os.path.basename(source_file_path)
        article_name = os.path.splitext(article_base_name)

        source_code = SourceReader.get_source(source_file_path)
        source_code = source_replacer.replace_styles(source_code)
        include_counter = reference_finder.has_include(source_file_path)
        if include_counter == 1:
            source_code = file_maker.replace_main_file_includes(source_code)
        source_code = source_replacer.replace_media_references(source_code, source_file_path, "/opt/lampp/htdocs/Blog/")
        source_code = source_replacer.replace_link_references(source_code)
        article_register.register_article(source_code, article_name[0])
        article_id = component_retriever.get_article_id("article " + article_name[0])

        article_register.register_menu_item(article_id, "Article " + article_name[0])
