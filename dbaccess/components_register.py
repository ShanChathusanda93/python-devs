import datetime
import time

import pymysql

from dbaccess.component_retriever import ComponentRetriever


class ComponentRegistry:
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

    def register_module(self, module_name):
        current_time = datetime.datetime.now()
        date_string = str(current_time.month) + " " + str(current_time.year)
        try:
            connection = self.get_database_connection()
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

    def register_article(self, article_source, article_name):
        try:
            connection = self.get_database_connection()
            with connection.cursor() as cursor:
                # --defining the assets table values
                # --get the last inserted asset id
                get_last_asset_id_sql = "SELECT `id`, `asset_id` FROM `fa64n_content` ORDER BY `id` DESC " \
                                        "LIMIT 1;"
                cursor.execute(get_last_asset_id_sql)
                last_asset_id = ""
                last_lft = ""
                last_rgt = ""
                for row in cursor:
                    last_asset_id = row[1]

                # --get the lft and rgt values from last article in asset table
                get_lft_rgt_sql = "SELECT lft, rgt FROM fa64n_assets WHERE id = %s"
                cursor.execute(get_lft_rgt_sql, last_asset_id)
                for r in cursor:
                    last_lft = r[0]
                    last_rgt = r[1]

                # --get the article id to be inserted to the content table
                get_next_article_id = "SELECT AUTO_INCREMENT FROM information_schema.TABLES WHERE TABLE_SCHEMA = " \
                                      "\"JoomlaResearchTestSitedb\" AND TABLE_NAME =\"fa64n_content\";"
                cursor.execute(get_next_article_id)
                next_article_id = ""
                for art_id in cursor:
                    next_article_id = art_id[0]

                parent_id = 39
                lft = last_lft + 1
                rgt = last_rgt + 1
                level = 3
                name = "com.content.article." + str(next_article_id)
                title = "Article " + article_name
                rules = "{}"
                set_article_asset_sql = "INSERT INTO `fa64n_assets` (`parent_id`, `lft`, `rgt`, `level`, " \
                                        "`name`, `title`, `rules`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(set_article_asset_sql,
                               (str(parent_id), str(lft), str(rgt), str(level), name, title, rules))

                # --get the inserted asset id
                get_asset_id_sql = "SELECT `id` FROM `fa64n_assets` WHERE name = %s;"
                cursor.execute(get_asset_id_sql, name)
                asset_id = ""
                for aid in cursor:
                    asset_id = aid[0]

                # --register the article in content table
                alias = title.lower().replace(" ", "-")
                introtext = "<p>" + article_source + "</p>"
                state = 1
                catid = 14
                created = datetime.datetime.now() - datetime.timedelta(hours=5)
                created_by = 412
                modified = created
                modified_by = 0
                checked_out = 412
                checked_out_time = created
                publish_up = created
                images = '{"image_intro":"","float_intro":"","image_intro_alt":"","image_intro_caption":"",' \
                         '"image_fulltext":"","float_fulltext":"","image_fulltext_alt":"","image_fulltext_caption":""}'
                urls = '{"urla":false,"urlatext":"","targeta":"","urlb":false,"urlbtext":"","targetb":"",' \
                       '"urlc":false,"urlctext":"","targetc":""}'
                attribs = '{"article_layout":"","show_title":"","link_titles":"","show_tags":"","show_intro":"",' \
                          '"info_block_position":"","info_block_show_title":"","show_category":"","link_category":"",' \
                          '"show_parent_category":"","link_parent_category":"","show_associations":"",' \
                          '"show_author":"","link_author":"","show_create_date":"","show_modify_date":"",' \
                          '"show_publish_date":"","show_item_navigation":"","show_icons":"","show_print_icon":"",' \
                          '"show_email_icon":"","show_vote":"","show_hits":"","show_noauth":"","urls_position":"",' \
                          '"alternative_readmore":"","article_page_title":"","show_publishing_options":"",' \
                          '"show_article_options":"","show_urls_images_backend":"","show_urls_images_frontend":""}'
                version = 1
                ordering = 0
                access = 1
                hits = 0
                metadata = "{\"robots\":\"\",\"author\":\"\",\"rights\":\"\",\"xreference\":\"\"}"
                featured = 0
                language = "*"
                register_article_sql = "INSERT INTO `fa64n_content` (`asset_id`, `title`, `alias`, `introtext`, " \
                                       "`state`, `catid`, `created`, `created_by`, `modified`, `modified_by`, " \
                                       "`checked_out`, `checked_out_time`, `publish_up`, `images`, `urls`, `attribs`, " \
                                       "" \
                                       "" \
                                       "`version`, `ordering`, `access`, `hits`, `metadata`, `featured`, `language`) " \
                                       "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
                cursor.execute(register_article_sql, (str(asset_id), title, alias, introtext, str(state), str(catid),
                                                      str(created), str(created_by), str(modified), str(modified_by),
                                                      str(checked_out), str(checked_out_time), str(publish_up),
                                                      str(images), str(urls), str(attribs), str(version),
                                                      str(ordering), str(access), str(hits), str(metadata),
                                                      str(featured), str(language)))

                # --get last inserted article id
                get_last_article_id_sql = "SELECT `id` FROM `fa64n_content` ORDER BY `id` DESC LIMIT 1;"
                cursor.execute(get_last_article_id_sql)
                last_article_id = ""
                for row in cursor:
                    last_article_id = row[0]
                connection.commit()
                return last_article_id
        except pymysql.err.DatabaseError as error:
            print("Error occurred while the module registration. " + str(error.args[0]) + "," + str(error.args[1]))
            connection.rollback()

    def register_menu_item(self, article_id, article_title):
        component_retriever = ComponentRetriever()
        try:
            connection = self.get_database_connection()
            with connection.cursor() as cursor:
                last_menu_item_details = component_retriever.get_last_inserted_menu_item()
                menu_type = "mainmenu"
                title = article_title
                alias = article_title.lower().replace(" ", "-")
                path = alias
                link = "index.php?option=com_content&view=article&id=" + str(article_id)
                component_type = "component"
                published = 1
                parent_id = 1
                level = 1
                component_id = 22
                checked_out = 0
                checked_out_time = datetime.datetime.now() - datetime.timedelta(hours=5)
                browser_nav = 0
                access = 1
                template_style_id = 0
                params = '{"show_title":"","link_titles":"","show_intro":"","info_block_position":"",' \
                         '"info_block_show_title":"","show_category":"","link_category":"","show_parent_category":"",' \
                         '"link_parent_category":"","show_associations":"","show_author":"","link_author":"",' \
                         '"show_create_date":"","show_modify_date":"","show_publish_date":"",' \
                         '"show_item_navigation":"","show_vote":"","show_icons":"","show_print_icon":"",' \
                         '"show_email_icon":"","show_hits":"","show_tags":"","show_noauth":"","urls_position":"",' \
                         '"menu-anchor_title":"","menu-anchor_css":"","menu_image":"","menu_image_css":"",' \
                         '"menu_text":1,"menu_show":1,"page_title":"","show_page_heading":"","page_heading":"",' \
                         '"pageclass_sfx":"","menu-meta_description":"","menu-meta_keywords":"","robots":"","secure":0}'
                lft = last_menu_item_details[1] + 2
                rgt = last_menu_item_details[2] + 2
                home = 0
                language = "*"
                client_id = 0

                register_meu_item_sql = "INSERT INTO `fa64n_menu` (`menutype`, `title`, `alias`, `path`, `link`, " \
                                        "`type`, `published`, `parent_id`, `level`, `component_id`, `checked_out`, " \
                                        "`checked_out_time`, `browserNav`, `access`, `template_style_id`, `params`, " \
                                        "`lft`, `rgt`, `home`, `language`, `client_id`) VALUES(%s,%s,%s,%s,%s,%s,%s," \
                                        "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
                cursor.execute(register_meu_item_sql, (menu_type, title, alias, path, link, component_type, str(published),
                                                       str(parent_id), str(level), str(component_id),
                                                       str(checked_out), str(checked_out_time), str(browser_nav),
                                                       str(access), str(template_style_id), params, str(lft),
                                                       str(rgt), str(home), language, str(client_id)))
            connection.commit()
        except pymysql.err.DatabaseError as error:
            print("Error occurred while the module registration. " + str(error.args[0]) + "," + str(error.args[1]))
            connection.rollback()

    # def get_asset(self):
    #     connection = self.get_database_connection()
    #     with connection.cursor() as cursor:
    #         sql = "SELECT * FROM fa64n_assets ORDER BY id DESC LIMIT 1;"
    #         cursor.execute(sql)
    #         for row in cursor:
    #             print(row)
    #
    # def test_set(self):
    #     connection = self.get_database_connection()
    #     with connection.cursor() as cursor:
    #         sql = "INSERT INTO `admin_details` (`user_name`,`pass_for_user`,`role`) VALUES ('Test User',
    #         'Test pass', " \
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
# art_id = comp_reg.register_article("This is the article 004 file for the testing\n This is a new line.",
#                                    "Test article 004")
# print(str(art_id))
