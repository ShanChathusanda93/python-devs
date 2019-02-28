import pymysql


def connect_database():
    host = "localhost"
    user = "root"
    password = ""
    database = "JoomlaResearchTestSitedb"
    db = pymysql.connect(host, user, password, database)
    return db
