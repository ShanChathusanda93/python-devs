import re


class ConnectionCreator:
    # --need to develop this method to detect the connection variable from the mysql_connect()
    def get_connection_variable(self, connection_file_path):
        with open(connection_file_path, "r") as file:
            source = file.read().replace("\n", " ")
        words = source.split(";")
        match = [s for s in words if "mysqli_connect(" in s]
        connection_var = re.findall("\$(.*?)=", match[0])
        return connection_var[0]

    # --need to consider about whether this connection file stays as a file or a module
    def create_database_connection_file(self, connection_var, server_name, username, password, db_name):
        connection_string = "<?php\n" \
                            "/***\n" \
                            "*@package Joomla.Site\n" \
                            "*@subpackage mod_any_package\n" \
                            "*@license GNU/GPL, see LICENSE.php\n" \
                            "@copyright Copyright (C) 2005 - 2018, Open Source Matters, Inc. All rights " \
                            "reserved.\n" \
                            "***/\n" \
                            "// no direct access\n" \
                            "defined('_JEXEC') or die;\n" \
                            "// defining connection variables\n" \
                            "define('DB_SERVER', '" + server_name + "');\n" \
                            "define('DB_USERNAME', '" + username + "');\n" \
                            "define('DB_PASSWORD', '" + password + "');\n" \
                            "define(DB_NAME', '" + db_name + "');\n\n" \
                            "$" + connection_var + " = mysqli_connect(DB_SERVER, DB_USERNAME, DB_PASSWORD," \
                            "DB_NAME);\nif($" + connection_var + " == false){" \
                            "\n\tdie('Error, " \
                            "could not " \
                            "connect.' . " \
                            "mysqli_connect_error());\n}\n?>"
        # --user input
        target_base_dir_path = "/home/shan/Developments/Projects/research-devs/python-devs/filehandler"
        target_conn_dir_path = target_base_dir_path + "/phpSnippets/dbconnection"
        # dir_maker.create_target_directory(target_conn_dir_path)
        connection_file_path = target_conn_dir_path + "/connection.php"
        with open(connection_file_path, "w") as con_file:
            con_file.write(connection_string)

    def get_new_database_access_file(self):
        with open("/home/shan/Developments/Projects/research-devs/python-devs/filehandler/phpSnippets/dbconnection"
                  "/connection.php") as conn_file:
            conn_string = conn_file.read()
        return conn_string


# con_creator = ConnectionCreator()
# con_creator.create_database_connection_file("con", "localhost", "root", "", "JoomlaResearchTestSitedb")
# db_file = con_creator.get_new_database_access_file()
# with open("/home/shan/Developments/Projects/research-devs/python-devs/filehandler/phpSnippets/dbconnection"
#           "/connection_extended.php", "w+") as connection_file:
#     connection_file.write(db_file)
