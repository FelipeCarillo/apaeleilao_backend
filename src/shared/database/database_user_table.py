from typing import Dict, List
from src.shared.database.database import Database
from src.shared.structure.entities.user import User
from src.shared.structure.interface.user_interface import UserInterface


class UserTable(UserInterface):

    def __init__(self):
        self.__table = Database().get_table_user()

    def create_user(self, user: User):
        try:
            self.__table.insert_one(
                user.to_dict()
            )

            return {
                'statusCode': 201,
                'body': user.to_dict()
            }
        except Exception as e:
            return e

    def authenticate(self, _id, password) -> Dict or None:
        try:
            response = self.__table.find_one({'_id': _id, 'password': password})
            if response is not None:
                return response
            else:
                return None
        except Exception as e:
            return e

    def get_all_users(self) -> List[Dict] or None:
        try:
            response = list(self.__table.find())
            return response if len(response) > 0 else None
        except Exception as e:
            return e

    def get_user_by_id(self, _id) -> Dict or None:
        try:
            user = self.__table.find_one({'_id': _id})
            return user
        except Exception as e:
            return e

    def get_user_by_email(self, email) -> User or None:
        try:
            user = self.__table.find_one({'email': email})
            return user
        except Exception as e:
            return e

    def get_user_by_cpf(self, cpf) -> User or None:
        try:
            user = self.__table.find_one({'cpf': cpf})
            return user
        except Exception as e:
            return e

    def update_user(self, user: User):
        try:
            update_result = self.__table.update_one(
                {'_id': user.id},
                {'$set': user.to_dict()}
            )
            return update_result.raw_result
        except Exception as e:
            return str(e)
