import pytest
from src.shared.errors.modules_errors import InvalidParameter, MissingParameter
from src.shared.errors.usecase_errors import DataAlreadyUsed
from src.modules.create_user.app.create_user_usecase import CreateUserUseCase
from src.shared.structure.repository.user_repository_mock import UserRepositoryMock


class TestCreateUserUseCase:
    new_email = 'teste@testeste.com'
    new_cpf = '43213321422'

    def test_create_user_usecase(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUseCase(repo)
        user_test = repo.users[0].to_dict()
        response = usecase(email=self.new_email, cpf=self.new_cpf, first_name=user_test['first_name'],
                           last_name=user_test['last_name'], phone=user_test['phone'],
                           password=user_test['password'], accepted_terms=user_test['accepted_terms'])

        assert response['first_name'] == user_test['first_name']
        assert response['last_name'] == user_test['last_name']
        assert response['cpf'] == self.new_cpf
        assert response['email'] == self.new_email
        assert response['phone'] == user_test['phone']
        assert response['password'] == user_test['password']
        assert response['accepted_terms'] == user_test['accepted_terms']
        assert response['status_account'] == user_test['status_account'].value
        assert response['suspensions'] == user_test['suspensions']
        assert response['date_joined'] == user_test['date_joined']
        assert response['verification_email_code'] == user_test['verification_email_code']
        assert response['verification_email_code_expires_at'] == user_test['verification_email_code_expires_at']
        assert response['password_reset_code'] == user_test['password_reset_code']
        assert response['password_reset_code_expires_at'] == user_test['password_reset_code_expires_at']

    def test_create_user_usecase_with_email_already_used(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUseCase(repo)
        user_test = repo.users[0].to_dict()
        with pytest.raises(DataAlreadyUsed) as exc:
            usecase(email=user_test['email'], cpf=self.new_cpf, first_name=user_test['first_name'],
                    last_name=user_test['last_name'], phone=user_test['phone'],
                    password=user_test['password'], accepted_terms=user_test['accepted_terms'])
        assert str(exc.value) == 'Parameter email already used.'

    def test_create_user_usecase_with_cpf_already_used(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUseCase(repo)
        user_test = repo.users[0].to_dict()
        with pytest.raises(DataAlreadyUsed) as exc:
            usecase(email=self.new_email, cpf=user_test['cpf'], first_name=user_test['first_name'],
                    last_name=user_test['last_name'], phone=user_test['phone'],
                    password=user_test['password'], accepted_terms=user_test['accepted_terms'])
        assert str(exc.value) == 'Parameter cpf already used.'

    def test_create_user_usecase_with_invalid_request(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUseCase(repo)
        user_test = repo.users[0].to_dict()
        with pytest.raises(MissingParameter) as exc:
            usecase(email=None, cpf=self.new_cpf, first_name=user_test['first_name'],
                    last_name=user_test['last_name'], phone=user_test['phone'],
                    password=user_test['password'], accepted_terms=user_test['accepted_terms'])
        assert str(exc.value) == 'Missing email parameter.'

    def test_create_user_usecase_with_invalid_parameter(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUseCase(repo)
        user_test = repo.users[0].to_dict()
        with pytest.raises(InvalidParameter) as exc:
            usecase(email=self.new_email, cpf=748, first_name=user_test['first_name'],
                    last_name=user_test['last_name'], phone=user_test['phone'],
                    password=user_test['password'], accepted_terms=user_test['accepted_terms'])
        assert str(exc.value) == "Invalid cpf parameter: deve ser str."
