import pytest
from src.modules.create_user.app.create_user_controller import CreateUserController
from src.modules.create_user.app.create_user_usecase import CreateUserUseCase
from src.shared.structure.repository.user_repository_mock import UserRepositoryMock

class TestCreateUserController:
    repo = UserRepositoryMock()
    usecase = CreateUserUseCase(repo)
    controller = CreateUserController(usecase)

    def test_create_user_controller(self):
        email = 'teste@testeste.com'
        cpf = '43213321422'
        request = {
            'body': {
                'email': email,
                'cpf': cpf,
                'first_name': self.repo.users[0].first_name,
                'last_name': self.repo.users[0].last_name,
                'phone': self.repo.users[0].phone,
                'password': self.repo.users[0].password,
                'accepted_terms': self.repo.users[0].accepted_terms
            }
        }

        response = self.controller(request=request)

        assert response.status_code == 201
        assert response.body['user']['email'] == email
        assert response.body['user']['password'] == self.repo.users[0].password
