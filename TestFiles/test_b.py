from dataobjects.detail_keeper_do import DetailsKeeperDO


class B:
    def set_source_path(self, source_path):
        DetailsKeeperDO.set_source_dir_path(DetailsKeeperDO, source_path)
