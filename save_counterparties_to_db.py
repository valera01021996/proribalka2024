import requests
from database.tools.base_tools import BaseTools
from dotenv import load_dotenv
import os
load_dotenv()


class SaveCounterparties(BaseTools):

    def do_request(self):
        response = requests.get("https://online.moysklad.ru/api/remap/1.2/entity/counterparty",
                                auth=(os.getenv("LOGIN_MOYSKLAD"), os.getenv("PASSWORD_MOYSKLAD"))).json()
        return response

    def add_counterparty_to_db(self, name, date_of_birth, phone, group_name, discountcardnumber, bonus):
        try:
            self.cursor.execute("""INSERT INTO counterparties(name, date_of_birth, phone, group_name, discountcardnumber, bonus)
                VALUES(
                %s,
                %s,
                %s,
                %s,
                %s,
                %s)
                ON DUPLICATE KEY UPDATE
                name = VALUES(name),
                date_of_birth = VALUES(date_of_birth),
                phone = VALUES(phone),
                group_name = VALUES(group_name),
                discountcardnumber = VALUES(discountcardnumber),
                bonus = VALUES(bonus)

            """, (name, date_of_birth, phone, group_name, discountcardnumber, bonus))

        except Exception as ex:
            print(ex)

        else:
            self.connection.commit()

    def gather_info_counterparty(self):
        response = SaveCounterparties().do_request()
        try:
            for dict_ in response["rows"]:
                try:
                    try:
                        name = dict_["name"]
                        print(name)
                    except:
                        name = "Нет имени"
                    try:
                        date_of_birth = dict_["description"]
                        print(date_of_birth)
                    except:
                        date_of_birth = "Нет даты"
                    try:
                        phone = dict_["phone"]
                        if "(" in phone:
                            phone = phone.replace("(", "")
                        if ")" in phone:
                            phone = phone.replace(")", "")
                        if "-" in phone:
                            phone = phone.replace("-", "")
                        if " " in phone:
                            phone = phone.replace(" ", "")
                    except:
                        phone = "Нет номера телефона"
                    try:
                        group_name = dict_["tags"]
                    except:
                        group_name = "Нет группы"
                    try:
                        discountcardnumber = dict_["discountCardNumber"]
                    except:
                        discountcardnumber = "Нет карты"
                    try:
                        bonus = dict_["bonusPoints"]
                    except:
                        bonus = "Нет бонусов"
                    SaveCounterparties().add_counterparty_to_db(name, date_of_birth, phone, group_name,
                                                                discountcardnumber, bonus)
                except Exception as ex:
                    print(ex)

                print("Success")

        except Exception as ex:
            print(ex)


SaveCounterparties().gather_info_counterparty()
