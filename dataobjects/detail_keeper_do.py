class DetailsKeeperDO:
    source_dir_path = ""
    source_file_list = []
    avoided_file_list = []
    db_conn_file_path = ""

    @staticmethod
    def set_source_dir_path(self, source_dir_path):
        self.source_dir_path = source_dir_path

    @staticmethod
    def get_source_dir_path(self):
        return self.source_dir_path

    def set_source_file_list(self, source_file_list):
        self.source_file_list = source_file_list

    def get_source_file_list(self):
        return self.source_file_list

    @staticmethod
    def set_avoided_file_list(self, avoided_file_list):
        self.avoided_file_list = avoided_file_list

    @staticmethod
    def get_avoided_file_list(self):
        return self.avoided_file_list

    def add_avoided_files(self, file_list):
        self.avoided_file_list.extend(file_list)

    @staticmethod
    def set_db_conn_file(self, db_conn_file_path):
        self.db_conn_file_path = db_conn_file_path

    @staticmethod
    def get_db_conn_file(self):
        return self.db_conn_file_path
