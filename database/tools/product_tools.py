from .base_tools import BaseTools


class ProductTools(BaseTools):
    CATEGORIES = []
    SUBCATEGORIES = []
    BRANDS = []
    SERIES = []
    TYPES = []
    TYPES2 = []
    PRODUCTS = []

    def get_categories(self) -> list:
        self.cursor.execute("""SELECT DISTINCT category_name
            FROM products
            ORDER BY category_name ASC
        """)
        categories = []
        for category in self.cursor.fetchall():
            categories.append(*category)
        ProductTools.CATEGORIES = categories
        return categories

    def get_subcategories(self, category_name: str) -> list:
        self.cursor.execute("""SELECT DISTINCT subcategory_name
            FROM products
            WHERE category_name = %s
            ORDER BY subcategory_name ASC
        """, (category_name,))
        subcategories = []
        for subcategory in self.cursor.fetchall():
            subcategories.append(*subcategory)
        ProductTools.SUBCATEGORIES = subcategories
        return subcategories

    def get_brands(self, subcategory_name: str) -> list:
        self.cursor.execute("""SELECT DISTINCT brand_name
            FROM products
            WHERE subcategory_name = %s
            ORDER BY brand_name ASC
        """, (subcategory_name,))
        brands = []
        for brand in self.cursor.fetchall():
            brands.append(*brand)

        ProductTools.BRANDS = brands
        return brands

    def get_brands_without_subcategories(self, category_name: str) -> list:
        self.cursor.execute("""SELECT DISTINCT brand_name
            FROM products
            WHERE category_name = %s
            ORDER BY brand_name ASC
        """, (category_name,))
        brands = []
        for brand in self.cursor.fetchall():
            brands.append(*brand)
        ProductTools.BRANDS = brands
        return brands

    def get_series_without_subcategory(self, category_name: str, brand_name: str) -> list:
        self.cursor.execute("""SELECT DISTINCT serie_name
            FROM products
            WHERE category_name = %s and brand_name = %s
            ORDER BY serie_name ASC
        """, (category_name, brand_name))
        series = []
        for serie in self.cursor.fetchall():
            series.append(*serie)
        ProductTools.SERIES = series
        return series

    def get_series(self, subcategory_name: str, brand_name: str) -> list:
        self.cursor.execute("""SELECT DISTINCT serie_name
            FROM products
            WHERE subcategory_name = %s and brand_name = %s
            ORDER BY serie_name ASC
        """, (subcategory_name, brand_name))
        series = []
        for serie in self.cursor.fetchall():
            series.append(*serie)
        ProductTools.SERIES = series
        return series


    def get_products(self, category_name: str) -> list:
        self.cursor.execute("""SELECT DISTINCT product_name
            FROM products
            WHERE category_name = %s
            ORDER BY product_name ASC
        """, (category_name,))
        products = []
        for product in self.cursor.fetchall():
            products.append(*product)
        ProductTools.PRODUCTS = products
        return products

    def get_products_without_subcategories(self, category_name: str, brand_name: str):
        self.cursor.execute("""SELECT DISTINCT product_name
            FROM products
            WHERE category_name = %s and brand_name = %s
            ORDER BY product_name ASC
        """, (category_name, brand_name))
        products = []
        for product in self.cursor.fetchall():
            products.append(*product)
        ProductTools.PRODUCTS = products
        return products

    def get_products_with_subcategories(self, category_name: str, subcategory_name: str) -> list:
        self.cursor.execute("""SELECT DISTINCT product_name
            FROM products
            WHERE category_name = %s and subcategory_name = %s
            ORDER BY product_name ASC
        """, (category_name, subcategory_name))
        products = []
        for product in self.cursor.fetchall():
            products.append(*product)
        ProductTools.PRODUCTS = products
        return products

    def get_products_with_brands(self, subcategory_name: str, brand_name: str) -> list:
        self.cursor.execute("""SELECT DISTINCT product_name
            FROM products
            WHERE subcategory_name = %s and brand_name = %s
            ORDER BY product_name ASC
        """, (subcategory_name, brand_name))
        products = []
        for product in self.cursor.fetchall():
            products.append(*product)
        ProductTools.PRODUCTS = products
        return products

    def get_products_with_series(self, brand_name: str, serie_name: str):
        self.cursor.execute("""SELECT DISTINCT product_name
            FROM products
            WHERE brand_name = %s and serie_name = %s
            ORDER BY product_name ASC
        """, (brand_name, serie_name))
        products = []
        for product in self.cursor.fetchall():
            products.append(*product)
        ProductTools.PRODUCTS = products
        return products

    def get_products_with_types(self, serie_name: str, type_name: str):
        self.cursor.execute("""SELECT DISTINCT product_name
            FROM products
            WHERE serie_name = %s and type_name = %s
            ORDER BY product_name ASC
        """, (serie_name, type_name))
        products = []
        for product in self.cursor.fetchall():
            products.append(*product)
        ProductTools.PRODUCTS = products
        return products

    def get_products_with_types2(self, type_name: str, type_name2: str):
        self.cursor.execute("""SELECT DISTINCT product_name
            FROM products
            WHERE type_name = %s and type_name2 = %s
            ORDER BY product_name ASC
        """, (type_name, type_name2))
        products = []
        for product in self.cursor.fetchall():
            products.append(*product)
        ProductTools.PRODUCTS = products
        return products

    def get_product_detail_info(self, product_name: str):
        self.cursor.execute("""SELECT id, product_name, description, image, price, quantity
            FROM products
            WHERE product_name = %s
        """, (product_name,))
        product: tuple = self.cursor.fetchone()
        return product

    def get_types(self, category_name: str, brand_name: str, serie_name: str):
        self.cursor.execute("""SELECT DISTINCT type_name
            FROM products
            WHERE category_name = %s and brand_name = %s and serie_name = %s
            ORDER BY type_name ASC
        """, (category_name, brand_name, serie_name))
        types = []
        for type_name in self.cursor.fetchall():
            types.append(*type_name)
        ProductTools.TYPES = types
        return types

    def get_types2(self, serie_name: str, type_name: str):
        self.cursor.execute("""SELECT DISTINCT type_name2
            FROM products
            WHERE serie_name = %s and type_name = %s
            ORDER BY type_name2 ASC
        """, (serie_name, type_name))
        types2 = []
        for type_name2 in self.cursor.fetchall():
            types2.append(*type_name2)
        ProductTools.TYPES2 = types2
        return types2

    def get_product_name_by_id(self, product_id):
        self.cursor.execute("""SELECT product_name
            FROM products
            WHERE id = %s
        """, (product_id,))
        product_name = self.cursor.fetchone()[0]
        return product_name

    def minus_count_units_in_store(self, quantity, title):
        self.cursor.execute("""UPDATE products
            SET quantity = quantity - %s
            WHERE product_name = %s
        """, (quantity, title))
        self.connection.commit()

    def delete_product(self):
        self.cursor.execute("""
            DELETE from products
            WHERE quantity = 0
        """)
        self.connection.commit()
