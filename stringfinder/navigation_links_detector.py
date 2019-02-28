import re

from dataobjects.navigation_do import NavigationDO


class NavigationLinksDetector:
    def get_navigation_links(self, navigation_files_details):
        navigation_details = []
        for nav_file in navigation_files_details:
            links = []
            for nav_link in nav_file.navigations:
                navigators = re.findall("<a href=\"(.*?)\"", nav_link)
                for nav in navigators:
                    links.append(nav)
            navigation_do = NavigationDO()
            navigation_do.set_nav_file_name(nav_file.nav_file_name)
            navigation_do.set_navigations(links)
            navigation_details.append(navigation_do)
        return navigation_details

    # --this method will return the completed file paths to the navigated files by searching the file paths with the
    # main file list
    def get_navigated_file_paths(self, navigation_files_details, file_list):
        nav_details = []
        for nav in navigation_files_details:
            links = []
            for link in nav.navigations:
                if "../../" in link:
                    link = link.replace("../..", "")
                elif "../" in link:
                    link = link.replace("..", "")
                matching = [file for file in file_list if link in file]
                for match in matching:
                    links.append(match)
            navigation_do = NavigationDO()
            navigation_do.set_nav_file_name(nav.nav_file_name)
            navigation_do.set_navigations(links)
            nav_details.append(navigation_do)
        return nav_details
