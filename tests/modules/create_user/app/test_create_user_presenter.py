from src.modules.create_user.app.create_user_presenter import lambda_handler
from src.shared.structure.repository.user_repository_mock import UserRepositoryMock

class TestCreateUserPresenter:
    def test_create_user_presenter(self):
        repo = UserRepositoryMock()
        new_email = '23.00765-6@outlook.com'
        new_cpf = '43213321422'
        event = {
            'body': {
                'body': {
                    'email': new_email,
                    'cpf': new_cpf,
                    'first_name': repo.users[0].first_name,
                    'last_name': repo.users[0].last_name,
                    'phone': repo.users[0].phone,
                    'password': repo.users[0].password,
                    'accepted_terms': repo.users[0].accepted_terms
                }
            }
        }

        presenter = lambda_handler(event=event, context=None)

        assert presenter['statusCode'] == 201
        assert presenter['body']['user']['email'] == new_email
        assert presenter['body']['user']['password'] == repo.users[0].password


