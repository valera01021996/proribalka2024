from .base_tools import BaseTools


class CartTools(BaseTools):
    def get_active_cart(self, user_id: int) -> tuple:
        self.cursor.execute("""SELECT *
            FROM carts
            WHERE user_id =%s  AND in_order = 0
        """, (user_id,))
        cart: tuple = self.cursor.fetchone()
        return cart

    def register_cart(self, user_id: int):
        if not self.get_active_cart(user_id):
            self.cursor.execute("""INSERT INTO carts (user_id)
                VALUES (%s)
            """, (user_id,))
            self.connection.commit()

    def recalc_cart(self, cart_id: int):
        self.cursor.execute("""SELECT SUM(quantity), SUM(total_coast)
            FROM cart_products
            WHERE cart_id = %s
        """, (cart_id,))
        total_price, total_amount = self.cursor.fetchone()
        self.cursor.execute("""UPDATE carts
            SET total_price = %s, total_amount = %s
            WHERE cart_id = %s
        """, (total_amount, total_price, cart_id))
        self.connection.commit()

    def get_cart_product(self, user_id: int):
        cart_id = self.get_active_cart(user_id)[0]
        self.cursor.execute("""SELECT product_name
            FROM cart_products
            WHERE cart_id = %s
        """, (cart_id,))
        product_names = self.cursor.fetchall()
        return product_names

    def get_cart_product_id(self, product_name: str):
        self.cursor.execute("""SELECT product_id
            FROM cart_products
            WHERE product_name = %s
        """, (product_name,))
        product_id = self.cursor.fetchone()[0]
        return product_id

    def add_cart_product(self, cart_id: int, product_id: int, product_name: str, quantity: int,
                         total_coast: float) -> bool:
        status_add = False

        try:
            self.cursor.execute("""INSERT INTO cart_products
                (cart_id, product_id, product_name, quantity, total_coast)
                VALUES(%s, %s, %s, %s, %s)
            """, (cart_id, product_id, product_name, quantity, total_coast))
        except:
            self.cursor.execute("""UPDATE cart_products
            SET quantity = %s, total_coast = %s
            WHERE product_id = %s
            """, (quantity, total_coast, product_id))

        else:
            status_add = True

        finally:
            self.connection.commit()
            return status_add

    def get_cart_products(self, user_id: int):
        cart_id = self.get_active_cart(user_id)[0]
        self.cursor.execute("""SELECT product_id, product_name, quantity, total_coast
            FROM cart_products
            WHERE cart_id = %s
        """, (cart_id,))
        cart_products = self.cursor.fetchall()
        return cart_products

    def change_order_status(self, cart_id: int):
        self.cursor.execute("""UPDATE carts
            SET in_order = 1
            WHERE id = %s
        """, (cart_id,))
        self.connection.commit()

    def delete_product_from_cart(self, product_name: str, cart_id: int):
        self.cursor.execute("""DELETE FROM cart_products
            WHERE product_name = %s and cart_id = %s
        """, (product_name, cart_id))
        self.connection.commit()

    def delete_all_products_from_cart(self, cart_id: int):
        self.cursor.execute("""DELETE FROM cart_products
            WHERE cart_id = %s
            """, (cart_id,))
        self.connection.commit()
