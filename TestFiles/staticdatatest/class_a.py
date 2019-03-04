from dataobjects.detail_keeper_do import DetailsKeeperDO


class ClassA:
    def set_source_directory_path(self, directory_path):
        DetailsKeeperDO.set_source_dir_path(DetailsKeeperDO, directory_path)
