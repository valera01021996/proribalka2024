from .base_tools import BaseTools


class UserTools(BaseTools):
    def register_user(self, username: str, full_name: str, chat_id: int):
        try:
            self.cursor.execute("""INSERT INTO users(username, full_name, chat_id)
                VALUES(%s, %s, %s)
            """, (username, full_name, chat_id))
        except Exception as ex:
            print(ex)
        else:
            self.connection.commit()

    def save_phone_number(self, phone_number, chat_id):
        try:
            self.cursor.execute("""UPDATE users
                SET phone_number = %s
                WHERE chat_id = %s
            """, (phone_number, chat_id))
        except Exception as ex:
            print(ex)
        else:
            self.connection.commit()

    def get_phone_number(self, chat_id):
        self.cursor.execute("""SELECT phone_number
            FROM users
            WHERE chat_id = %s
        """, (chat_id,))
        phone_number = self.cursor.fetchone()[0]
        return phone_number

    def get_user_id(self, chat_id: int):
        self.cursor.execute("""SELECT id
        FROM users
        WHERE chat_id = %s
        """, (chat_id,))
        user_id = self.cursor.fetchone()[0]
        return user_id
