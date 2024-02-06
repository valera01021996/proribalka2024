from .base_tools import BaseTools


class AdminTools(BaseTools):


    def select_all_chat_ids(self):
        self.cursor.execute("""SELECT chat_id
        FROM users
        """)
        chat_ids = self.cursor.fetchall()
        return chat_ids
