class NavigationDO:
    # def __init__(self, nav_file_name, navigations):
    #     self.nav_file_name = nav_file_name
    #     self.navigations = navigations

    nav_file_name = ""
    navigations = []

    # def __init__(self):
    #     pass

    def set_nav_file_name(self, nav_file_name):
        self.nav_file_name = nav_file_name

    def set_navigations(self, navigations):
        self.navigations = navigations

    def get_nav_file_name(self):
        return self.nav_file_name

    def get_navigations(self):
        return self.navigations
