from database.utils import connect_to_database


class InitDB:
    def __init__(self):
        self.connection, self.cursor = connect_to_database()


    def __create_products_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS products(
            id INTEGER PRIMARY KEY AUTO_INCREMENT,
            product_name VARCHAR(150) NOT NULL,
            description VARCHAR(2000),
            category_name VARCHAR(50),
            subcategory_name VARCHAR(50),
            brand_name VARCHAR(50),
            serie_name VARCHAR(50),
            type_name VARCHAR(50),
            type_name2 VARCHAR(50),
            price VARCHAR(50),
            quantity VARCHAR(50),
            image VARCHAR(300),
            product_id VARCHAR(200) UNIQUE
        )""")


    def __create_bu_products_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS products_bu(
            id INTEGER PRIMARY KEY AUTO_INCREMENT,
            product_name VARCHAR(150) NOT NULL,
            description VARCHAR(2000),
            category_name VARCHAR(50),
            subcategory_name VARCHAR(50),
            brand_name VARCHAR(50),
            serie_name VARCHAR(50),
            type_name VARCHAR(50),
            price VARCHAR(50),
            quantity VARCHAR(50),
            image VARCHAR(300),
            product_id VARCHAR(200) UNIQUE
        )""")



    def init(self):
        self.__create_products_table()
        self.__create_bu_products_table()




if __name__ == "__main__":
    InitDB().init()





