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
            user_authenticated = []
            response = self.__table.find({'_id': _id, 'password': password})
            for item in response:
                user_authenticated.append(item)
            if len(user_authenticated) > 0:
                return user_authenticated[0]
            else:
                return None
        except Exception as e:
            return e

    def get_all_users(self) -> List[Dict] or None:
        try:
            users = []
            response = self.__table.find()
            for item in response:
                users.append(item)
            if len(users) > 0:
                return users
            else:
                return None
        except Exception as e:
            return e

    def get_user_by_id(self, _id) -> Dict or None:
        try:
            user = []
            for item in self.__table.find({'_id': _id}):
                user.append(item)
            if len(user) > 0:
                return user[0]
            else:
                return None
        except Exception as e:
            return e

    def get_user_by_email(self, email) -> User or None:
        try:
            user = []
            for item in self.__table.find({'email': email}):
                user.append(item)
            if len(user) > 0:
                return user[0]
            else:
                return None
        except Exception as e:
            return e

    def get_user_by_cpf(self, cpf) -> User or None:
        try:
            user = []
            for item in self.__table.find({'cpf': cpf}):
                user.append(item)
            if len(user) > 0:
                return user[0]
            else:
                return None
        except Exception as e:
            return e

    def update_user(self, user: User):
        try:
            user = self.__table.update_one(
                {'_id': user._id},
                {'$set': user.to_dict()}
            )
            return user
        except Exception as e:
            return e