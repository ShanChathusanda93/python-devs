import shutil
import os


class FileMigrator:
    def move_media_files(self, media_file_paths, target_media_dir_path):
        for media in media_file_paths:
            file_name = os.path.basename(media)
            shutil.copy2(media, target_media_dir_path + file_name)

    def create_footer_overload(self, source_file_path):
        with open(source_file_path) as source_file:
            source_code = source_file.read()
        with open("/opt/lampp/htdocs/JoomlaResearchTest/modules/mod_footer/tmpl/default.php", "r") as \
                footer_file:
            footer_source = footer_file.read()
        footer_source = footer_source + "\n" + source_code
        self.create_target_directory("/opt/lampp/htdocs/JoomlaResearchTest/templates/protostar/html/mod_footer")
        with open("/opt/lampp/htdocs/JoomlaResearchTest/templates/protostar/html/mod_footer/default.php", "w+") as \
                target_footer_file:
            target_footer_file.write(footer_source)

    def create_target_directory(self, directory_path):
        access_rights = 0o755
        if not os.path.exists(directory_path):
            os.mkdir(directory_path, access_rights)


file_mige = FileMigrator()
file_mige.create_footer_overload("/opt/lampp/htdocs/extended_blog/Template/Footer/footer.php")
