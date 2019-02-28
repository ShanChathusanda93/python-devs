import datetime
import time

import pymysql


class ComponentRegistry:
    def connect_database(self):
        host = "localhost"
        user = "root"
        password = ""
        database = "JoomlaResearchTestSitedb"
        try:
            db = pymysql.connect(host, user, password, database)
            return db
        except pymysql.err.DatabaseError as error:
            print("Error occurred while connecting to the database. " + str(error.args[0]) + " , " + error.args[1])

    def register_module(self, module_name):
        current_time = datetime.datetime.now()
        date_string = str(current_time.month) + " " + str(current_time.year)
        try:
            connection = self.connect_database()
            with connection.cursor() as cursor:
                # --installing the created module as an extension
                # --parameters
                extension_name = module_name
                element_type = "module"
                element = module_name
                client_id = 0
                enabled = 1
                access = 1
                protected = 0
                manifest_cache = "{\"name\":\"" + module_name + "\",\"type\":\"module\",\"creationDate\":" \
                                 + date_string + "\",\"author\":\"Joomla! Project\",\"copyright\":\"Copyright (C) \" \
                                 \"2005 - 2018 Open Source Matters. All rights \" \
                                 \"reserved.\",\"authorEmail\":\"your_email_goes_here\",\" \
                                 \"authorUrl\":\"your.website.com\",\"version\":\"1.1.0\",\"description\":" + \
                                 module_name + " module\" ,\"group\":"",\"filename\":" + module_name + "}"
                params = {}
                state = 0
                # --sql execution
                register_extension_sql = "INSERT INTO `fa64n_extensions` (`name`, `type`, `element`, `client_id`, " \
                                         "`enabled`, `access`, `protected`, `manifest_cache`, `params`, " \
                                         "`state`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(register_extension_sql, (str(extension_name), str(element_type), str(element),
                                                        str(client_id), str(enabled), str(access), str(protected),
                                                        str(manifest_cache),
                                                        params.__str__(), state.__str__()))
                # --get the last inserted asset id from the modules table to get the left and the right
                # --params
                get_id_sql = "SELECT `id`, `asset_id` FROM `fa64n_modules` ORDER BY `id` DESC LIMIT 1;"
                cursor.execute(get_id_sql)
                last_asset_id = ""
                last_lft = ""
                last_rgt = ""
                for row in cursor:
                    last_asset_id = row[1]
                get_asset_sql = "SELECT lft, rgt FROM fa64n_assets WHERE id = %s"
                cursor.execute(get_asset_sql, last_asset_id)
                for r in cursor:
                    last_lft = r[0]
                    last_rgt = r[1]
                # --get the next module id to be added to the modules table to make the module name
                get_next_module_id_sql = "SELECT AUTO_INCREMENT FROM information_schema.TABLES WHERE TABLE_SCHEMA = " \
                                         "\"JoomlaResearchTestSitedb\" AND TABLE_NAME =\"fa64n_modules\";"

                # --registering the created module in the asserts table
                cursor.execute(get_next_module_id_sql)
                module_id = ""
                for mod_id in cursor:
                    module_id = mod_id[0]

                parent_id = 18
                lft = last_lft + 2
                rgt = last_rgt + 2
                level = 2
                name = "com_modules.module." + str(module_id)
                title = module_name + " module for migrated site"
                rules = {}
                set_module_asset_sql = \
                    """INSERT INTO `fa64n_assets` (`parent_id`, `lft`, `rgt`, `level`, `name`, `title`, `rules`) 
                    VALUES (%s,%s,%s,%s,%s,%s,%s)"""
                cursor.execute(set_module_asset_sql, (parent_id.__str__(), lft.__str__(), rgt.__str__(),
                                                      level.__str__(), name.__str__(), title.__str__(), str(rules)))

                # --registering the created module in module table
                get_asset_id_sql = "SELECT `id` FROM `fa64n_assets` WHERE name = %s;"
                cursor.execute(get_asset_id_sql, name)
                asset_id = ""
                for aid in cursor:
                    asset_id = aid[0]

                ordering = 1
                checked_out = 0
                checked_out_time = "0000-00-00 00:00:00"
                publish_up = time.strftime('%Y-%m-%d %H:%M:%S')
                publish_down = "0000-00-00 00:00:00"
                published = 1
                module = module_name
                access = 1
                show_title = 1
                params = "{\"parent\": \"14\", \"module_tag\": \"div\", \"bootstrap_size\": \"0\", \"header_tag\": " \
                         "\"h3\", \"header_class\": \"\", \"style\": \"0\"}"
                client_id = 0
                language = "*"
                set_module_sql = "INSERT INTO `fa64n_modules` (`asset_id`, `title`, `ordering`, `checked_out` , " \
                                 "`checked_out_time` , `publish_up` , `publish_down` , `published` , `module` , " \
                                 "`access` , `showtitle`, `params`, `client_id`, `language`) " \
                                 "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(set_module_sql, (asset_id.__str__(), title.__str__(), ordering.__str__(),
                                                checked_out.__str__(), checked_out_time.__str__(),
                                                publish_up.__str__(), publish_down.__str__(), published.__str__(),
                                                module.__str__(), access.__str__(), show_title.__str__(),
                                                params.__str__(), client_id.__str__(), language.__str__()))
            connection.commit()
            return title
        except pymysql.err.DatabaseError as err:
            print("Error occurred while the module registration. " + str(err.args[0]) + "," + str(err.args[1]))
            connection.rollback()

    # def get_asset(self):
    #     connection = self.connect_database()
    #     with connection.cursor() as cursor:
    #         sql = "SELECT * FROM fa64n_assets ORDER BY id DESC LIMIT 1;"
    #         cursor.execute(sql)
    #         for row in cursor:
    #             print(row)
    #
    # def test_set(self):
    #     connection = self.connect_database()
    #     with connection.cursor() as cursor:
    #         sql = "INSERT INTO `admin_details` (`user_name`,`pass_for_user`,`role`) VALUES ('Test User', 'Test pass', " \
    #               "" \
    #               "" \
    #               "" \
    #               "" \
    #               "'Test role'); "
    #         cursor.execute(sql)
    #     connection.commit()


# comp_reg = ComponentRegistry()
# comp_reg.register_module("python test module")
# comp_reg.get_asset()
# comp_reg.test_set()
