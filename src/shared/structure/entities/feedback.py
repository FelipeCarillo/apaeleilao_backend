from abc import ABC
import re

from src.shared.errors.modules_errors import *


class Feedback(ABC):
    feedback_id: str
    email: str
    content: str
    created_at:int
   
    def __init__(self,feedback_id:str=None, email:str=None,content:str=None,created_at:int=None) -> None:
        self.feedback_id = feedback_id
        self.email = self.validate_and_set_email(email)
        self.content = self.validate_and_set_content(content)
        self.created_at = created_at
    
    def to_dict(self):
        return {
            "feedback_id":self.feedback_id,
            "email":self.email,
            "content":self.content,
            "created_at":self.created_at
        }

    @staticmethod
    def validate_and_set_email(email: str) -> str:
        if email is None:
            raise MissingParameter("Email")
        if re.fullmatch(r"[A-Za-z0-9.]+@[A-Za-z0-9.]+\.[A-Za-z]{2,}", email) is None:
            raise InvalidParameter("Email", "inválido")
        if not isinstance(email, str):
            raise InvalidParameter("Email", "deve ser str")
        return email
    
    @staticmethod
    def validate_and_set_content(content:str) -> str:
        if content is None:
            raise MissingParameter("Texto")
        if not isinstance(content,str):
            raise InvalidParameter("Texto", "deve ser str")
        if len(content) > 500:
            raise InvalidParameter("Texto", "deve ter menos de 500 caracteres")
