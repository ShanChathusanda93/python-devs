import pymysql


def po():
    with open('C:/Users/PycharmProjects/u2/Ntt.txt') as o:
        for i in o:
            return i


ccc = pymysql.connect(host='127.0.0.1', port=3306, user='root', password=po(), db='mysql')
bak = ccc.cursor()
print(bak.execute("SELECT User FROM mysql.user;"))

ccc.close()
bak.close()



# po()



# def connect_database():
#     host = "localhost"
#     user = "root"
#     password = ""
#     database = "JoomlaResearchTestSitedb"
#     db = pymysql.connect(host, user, password, database)
#     return db
