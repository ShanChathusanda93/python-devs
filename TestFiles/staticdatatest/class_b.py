from dataobjects.detail_keeper_do import DetailsKeeperDO


class ClassB:
    def get_source_directory_path(self):
        source_path = DetailsKeeperDO.get_source_dir_path(DetailsKeeperDO)
        return source_path
