import pytest

from src.shared.structure.entities.user import User, UserEntityError


class Test_User:
    def test_user(self):
        user = User(user_id="123456789012345678901234567890123456", first_name="John", last_name="Doe",
                    cpf="12345678901", email="john@gamil.com")

        assert user.user_id == "123456789012345678901234567890123456"
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.cpf == "12345678901"
        assert user.email == "john@gamil.com"

    def test_user_id_is_none(self):
        with pytest.raises(UserEntityError):
            User(user_id=None, first_name="John", last_name="Doe",
                 cpf="12345678901", email="deada@famail.com")

    def test_user_id_is_not_str(self):
        with pytest.raises(UserEntityError):
            User(user_id=123, first_name="John", last_name="Doe",
                 cpf="12345678901", email="deada@famail.com")
