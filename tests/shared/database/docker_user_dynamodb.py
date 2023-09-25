from tests.shared.database.docker_dynamodb import DockerDynamodb
from src.shared.structure.entities.user import User


class DockerUserDynamodb:
    test_user = User(
        user_id='e659e096-5cff-4bd0-9ec5-a86bca525803',
        first_name='Teste',
        last_name='Teste',
        email='teste@teste.com',
        phone='(11) 11111-1111',
        password='123456',
        cpf='111.111.111-11',
        date_joined=1695648337882020500,
        accepted_terms=True,
        is_verified=True,
    ).to_dict()

    def __init__(self):
        self.__dynamodb = DockerDynamodb().get_table_user()

    def create_user(self):
        try:
            if 'User_Apae_Leilao' not in self.__dynamodb.meta.client.list_tables()['TableNames']:
                print("The 'User_Apae_Leilao' table does not exist.")
                return None
            self.__dynamodb.put_item(
                Item=self.test_user)

        except Exception as e:
            raise e

    def update_user(self):
        pass

    def delete_user(self):
        pass

    def get_user_by_id(self, user_id):
        try:
            response = self.__dynamodb.get_item(
                Key={
                    'user_id': self.test_user['user_id']
                }
            )
            return response['Item']
        except Exception as e:
            raise e

