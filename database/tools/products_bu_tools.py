from .base_tools import BaseTools


class ProductToolsBU(BaseTools):
    CATEGORIES = []
    SUBCATEGORIES = []
    BRANDS = []
    SERIES = []
    PRODUCTS = []

    def get_categories(self) -> list:
        self.cursor.execute("""SELECT DISTINCT category_name
            FROM products_bu
            ORDER BY category_name ASC
        """)
        categories = []
        for category in self.cursor.fetchall():
            categories.append(*category)
        ProductToolsBU.CATEGORIES = categories
        return categories

    def get_subcategories(self, category_name: str) -> list:
        self.cursor.execute("""SELECT DISTINCT subcategory_name
            FROM products_bu
            WHERE category_name = %s
            ORDER BY subcategory_name ASC
        """, (category_name,))
        subcategories = []
        for subcategory in self.cursor.fetchall():
            subcategories.append(*subcategory)
        ProductToolsBU.SUBCATEGORIES = subcategories
        return subcategories

    def get_brands_without_subcategories(self, category_name: str) -> list:
        self.cursor.execute("""SELECT DISTINCT brand_name
            FROM products_bu
            WHERE category_name = %s
            ORDER BY brand_name ASC
        """, (category_name,))
        brands = []
        for brand in self.cursor.fetchall():
            brands.append(*brand)

        ProductToolsBU.BRANDS = brands
        return brands

    def get_series(self, brand_name: str):
        self.cursor.execute("""SELECT DISTINCT serie_name
            FROM products_bu
            WHERE brand_name = %s
            ORDER BY serie_name ASC
        """, (brand_name,))
        series = []
        for serie in self.cursor.fetchall():
            series.append(*serie)
        ProductToolsBU.SERIES = series
        return series

    def get_products_without_brands(self, subcategory_name: str):
        self.cursor.execute("""SELECT DISTINCT product_name
            FROM products_bu
            WHERE subcategory_name = %s
            ORDER BY product_name ASC
        """, (subcategory_name,))
        products = []
        for product in self.cursor.fetchall():
            products.append(*product)

        ProductToolsBU.PRODUCTS = products
        return products

    def get_products_with_brands(self, category_name:str,  brand_name: str):
        self.cursor.execute("""SELECT DISTINCT product_name
            FROM products_bu
            WHERE category_name = %s and brand_name = %s
            ORDER BY product_name ASC
        """, (category_name, brand_name,))
        products = []
        for product in self.cursor.fetchall():
            products.append(*product)

        ProductToolsBU.PRODUCTS = products
        return products

    def get_products_with_series(self, brand_name, serie_name):
        self.cursor.execute("""SELECT DISTINCT product_name
            FROM products_bu
            WHERE brand_name = %s and serie_name = %s
            ORDER BY product_name ASC
        """, (brand_name, serie_name))
        products = []
        for product in self.cursor.fetchall():
            products.append(*product)

        ProductToolsBU.PRODUCTS = products
        return products

    def get_bu_product_detail_info(self, product_name: str):
        self.cursor.execute("""SELECT id, product_name, description, image, price, quantity
            FROM products_bu
            WHERE product_name = %s
        """, (product_name,))
        product: tuple = self.cursor.fetchone()
        return product

    def get_bu_product_name_by_id(self, product_id):
        self.cursor.execute("""SELECT product_name
            FROM products_bu
            WHERE id = %s
        """, (product_id,))
        product_name = self.cursor.fetchone()[0]
        return product_name

    def minus_bu_count_units_in_store(self, quantity, title):
        self.cursor.execute("""UPDATE products_bu
            SET quantity = quantity - %s
            WHERE product_name = %s
        """, (quantity, title))
        self.connection.commit()

    def delete_bu_product(self):
        self.cursor.execute("""
            DELETE from products_bu
            WHERE quantity = 0
        """)
        self.connection.commit()
