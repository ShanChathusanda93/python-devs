import pymysql


class ComponentRetriever:
    def get_database_connection(self):
        host = "localhost"
        user = "root"
        password = ""
        database = "JoomlaResearchTestSitedb"
        try:
            db = pymysql.connect(host, user, password, database)
            return db
        except pymysql.err.DatabaseError as error:
            print("Error occurred while connecting to the database. " + str(error.args[0]) + " , " + error.args[1])

    def get_article_id(self, article_name):
        try:
            connection = self.get_database_connection()
            article_name = article_name.lower().replace(" ", "-")
            with connection.cursor() as cursor:
                get_article_id_sql = "SELECT `id` FROM `fa64n_content` WHERE `alias` = %s;"
                cursor.execute(get_article_id_sql, article_name)
                for id_cursor in cursor:
                    return id_cursor[0]
            connection.commit()
        except pymysql.err.DatabaseError as err:
            print("Error occurred while the module registration. " + str(err.args[0]) + "," + str(err.args[1]))
            connection.rollback()

    def get_last_inserted_menu_item(self):
        try:
            connection = self.get_database_connection()
            with connection.cursor() as cursor:
                get_last_menu_item_sql = "SELECT `id`, `lft`, `rgt` FROM `fa64n_menu` WHERE `menutype` = %s ORDER BY " \
                                         "`id` DESC LIMIT 1;"
                cursor.execute(get_last_menu_item_sql, "mainmenu")
                menu_item_details = []
                for cursor_details in cursor:
                    menu_item_details.append(cursor_details)
            connection.commit()
            return menu_item_details
        except pymysql.err.DatabaseError as err:
            print("Error occurred while the module registration. " + str(err.args[0]) + "," + str(err.args[1]))
            connection.rollback()



comp_trt = ComponentRetriever()
# comp_trt.get_article_id("Article Test article 004")
# details = comp_trt.get_last_inserted_menu_item()
# for det in details:
#     print(det[1])
