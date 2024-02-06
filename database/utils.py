import pymysql


def connect_to_database() -> tuple:
    connection = pymysql.connect(
        host="10.10.10.149",
        database="proribalka",
        user="proribalka",
        password="Qwerty@123!"
    )
    cursor = connection.cursor()
    return connection, cursor


# connection, cursor = connect_to_database()
#
# cursor.execute(
#     """SELECT DISTINCT brand_name FROM products WHERE subcategory_name = 'Крючки'""")
# test = []
# for data in cursor.fetchall():
#     test.append(*data)
# print(test)
# def connect_to_database() -> tuple:
#     connection = pymysql.connect(
#         host="10.10.60.3",
#         database="iservice",
#         user="admin",
#         password=""
#     )
#     cursor = connection.cursor()
#     return connection, cursor
