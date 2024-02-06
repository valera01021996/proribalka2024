from .base_tools import BaseTools

class DriveTools(BaseTools):

    def select_phone_number_of_user(self, chat_id):
        self.cursor.execute("""SELECT phone_number
            FROM users
            WHERE chat_id = %s
        """, (chat_id, ))
        phone_number = self.cursor.fetchone()[0]
        return phone_number

    def select_bonus_of_user(self, phone_number):
        self.cursor.execute("""SELECT bonus
            FROM counterparties
            WHERE phone = %s
        """, (phone_number, ))
        bonus = self.cursor.fetchone()[0]
        return bonus

