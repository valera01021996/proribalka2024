from .base_tools import BaseTools


class ReviewTools(BaseTools):
    def save_review(self, user_id: int, full_name: str, phone_number: str, review: str):
        self.cursor.execute("""INSERT INTO reviews(user_id, full_name, phone_number, review)
            VALUES(%s, %s, %s, %s)
        """, (user_id, full_name, phone_number, review))
        self.connection.commit()

