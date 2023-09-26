import uuid
from src.shared.database.user_dynamodb import UserDynamodb
from src.shared.structure.entities.user import User


class CreateUserUseCase:
    def __init__(self, request):
        self.__request = request
        self.__dynamodb = UserDynamodb()

    def __call__(self):
        user = User(**self.__request['body'])
        user.user_id = str(uuid.uuid4())
        self.__dynamodb.create_user(user)
        return {
            'statusCode': 201,
            'body': user.to_dict()
        }
