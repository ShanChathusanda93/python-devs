import shutil
import os


class FileMigrator:
    def move_media_files(self, media_file_paths, target_media_dir_path):
        for media in media_file_paths:
            file_name = os.path.basename(media)
            shutil.copy2(media, target_media_dir_path + file_name)
