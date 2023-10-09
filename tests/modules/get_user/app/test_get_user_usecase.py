import pytest
from src.modules.get_user.app.get_user_usecase import GetUserUseCase
from src.shared.errors.modules_errors import MissingParameter, UserNotAuthenticated
from src.shared.structure.repository.user_repository_mock import UserRepositoryMock

class TestGetUserUsecase:
    def test_get_user_usecase(self):
        repo = UserRepositoryMock()
        usecase = GetUserUseCase(repo)
        user_test = repo.users[0].to_dict()
        response = usecase(email=user_test['email'], cpf=None, password=user_test['password'])

        assert response['user_id'] == user_test['user_id']
        assert response['first_name'] == user_test['first_name']
        assert response['last_name'] == user_test['last_name']
        assert response['cpf'] == user_test['cpf']
        assert response['email'] == user_test['email']
        assert response['phone'] == user_test['phone']

    def test_get_user_usecase_without_email(self):
        repo = UserRepositoryMock()
        usecase = GetUserUseCase(repo)
        user_test = repo.users[0].to_dict()
        with pytest.raises(MissingParameter) as exc:
            usecase(email=None, cpf=None, password=user_test['password'])
        assert str(exc.value) == 'Missing email or cpf parameter.'

    def test_get_user_usecase_without_password(self):
        repo = UserRepositoryMock()
        usecase = GetUserUseCase(repo)
        user_test = repo.users[0].to_dict()
        with pytest.raises(MissingParameter) as exc:
            usecase(email=user_test['email'], cpf=None, password=None)
        assert str(exc.value) == 'Missing password parameter.'

    def test_get_user_usecase_with_invalid_email(self):
        repo = UserRepositoryMock()
        usecase = GetUserUseCase(repo)
        user_test = repo.users[0].to_dict()
        with pytest.raises(MissingParameter) as exc:
            usecase(email='invalid_email', cpf=None, password=user_test['password'])
        assert str(exc.value) == 'Invalid email.'

    def test_get_user_usecase_with_invalid_cpf(self):
        repo = UserRepositoryMock()
        usecase = GetUserUseCase(repo)
        user_test = repo.users[0].to_dict()
        with pytest.raises(MissingParameter) as exc:
            usecase(email=None, cpf='invalid_cpf', password=user_test['password'])
        assert str(exc.value) == 'Invalid cpf.'

    def test_get_user_usecase_with_invalid_password(self):
        repo = UserRepositoryMock()
        usecase = GetUserUseCase(repo)
        user_test = repo.users[0].to_dict()
        with pytest.raises(UserNotAuthenticated) as exc:
            usecase(email=user_test['email'], cpf=None, password='invalid_password')
        assert str(exc.value) == 'User not authenticated.'






