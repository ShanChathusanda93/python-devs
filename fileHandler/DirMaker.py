import os


class DirectoryMaker:
    def make_directory(self, directory_path):
        access_rights = 0o755
        if not os.path.exists(directory_path):
            os.mkdir(directory_path, access_rights)
