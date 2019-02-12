import re

from fileHandler.NavigationDO import NavigationDO


class NavigationLinksDetector:
    def get_navigation_links(self, navigation_files_details):
        navigation_details = []
        for nav_file in navigation_files_details:
            links = []
            for nav_link in nav_file.navigations:
                navigators = re.findall("<a href=\"(.*?)\"", nav_link)
                for nav in navigators:
                    links.append(nav)
            navigation_details.append(NavigationDO(nav_file.nav_file_name, links))
        return navigation_details

    def get_navigated_file_paths(self, navigation_files_details, source_path):
        nav_details = []
        for nav in navigation_files_details:
            links = []
            for link in nav.navigations:
                file = ""
                if "../../" in link:
                    file = link.replace("../..", source_path)
                elif "../" in link:
                    file = link.replace("..", source_path)
                elif "/" in link:
                    file = source_path + link
                links.append(file)
            nav_details.append(NavigationDO(nav.nav_file_name, links))
        return nav_details
