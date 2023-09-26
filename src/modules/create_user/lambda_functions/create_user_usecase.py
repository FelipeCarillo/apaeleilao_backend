import uuid
from ....shared.database.user_dynamodb import UserDynamodb
from ....shared.structure.entities.user import User


class CreateUserUseCase:
    def __init__(self, request):
        self.__request = request
        self.__dynamodb = UserDynamodb()

    def __call__(self):
        auth = self.__dynamodb.authenticate(
            self.__request['auth']['user_id'],
            self.__request['auth']['password']
        )
        if not auth:
            return {
                'statusCode': 401,
                'body': 'Unauthorized'
            }

        user = User(**self.__request['body'])
        user.user_id = str(uuid.uuid4())
        self.__dynamodb.create_user(user)
        return {
            'statusCode': 201,
            'body': user.to_dict()
        }
