import re

from fileHandler.DirMaker import DirectoryMaker


class ConnectionCreator:
    # --need to develop this method to detect the connection variable from the mysql_connect()
    def get_connection_variable(self, connection_file_path):
        with open(connection_file_path, "r") as file:
            source = file.read().replace("\n", " ")
        words = source.split(";")
        match = [s for s in words if "mysqli_connect(" in s]
        connection_var = re.findall("\$(.*?)=", match[0])
        print(connection_var[0])
        return connection_var[0]

    # --need to consider about whether this connection file stays as a file or a module
    def create_database_connection_file(self, connection_var, server_name, username, password, db_name):
        dir_maker = DirectoryMaker()
        connection_string = "<?php\n$" + connection_var + " = mysqli_connect(\"" + server_name + "\",\"" + username + \
                            "\",\"" + password + "\",\"" + db_name + "\");\nif($" + connection_var + " == false){" \
                            "\ndie('Error, could not connect.' . mysqli_connect_error());\n}\n?>"
        # --user input
        target_base_dir_path = "/home/shan/Developments/Projects/research-devs/python-devs/fileHandler"
        target_conn_dir_path = target_base_dir_path + "/phpSnippets/dbconnection"
        dir_maker.make_directory(target_conn_dir_path)
        connection_file_path = target_conn_dir_path + "/connection.php"
        with open(connection_file_path, "w") as con_file:
            con_file.write(connection_string)
