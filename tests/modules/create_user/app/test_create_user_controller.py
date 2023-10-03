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
        assert response.body['first_name'] == self.repo.users[0].first_name
        assert response.body['last_name'] == self.repo.users[0].last_name
        assert response.body['cpf'] == cpf
        assert response.body['email'] == email
        assert response.body['phone'] == self.repo.users[0].phone
        assert response.body['password'] == self.repo.users[0].password
        assert response.body['accepted_terms'] == self.repo.users[0].accepted_terms
        assert response.body['status_account'] == self.repo.users[0].status_account
        assert response.body['suspensions'] == self.repo.users[0].suspensions
        assert response.body['date_joined'] == self.repo.users[0].date_joined
        assert type(response.body['verification_code']) == int
        assert len(str(response.body['verification_code'])) == 5
        assert response.body['verification_code_expires_at'] == self.repo.users[0].verification_code_expires_at
        assert response.body['password_reset_code'] == self.repo.users[0].password_reset_code
        assert response.body['password_reset_code_expires_at'] == self.repo.users[0].password_reset_code_expires_at
