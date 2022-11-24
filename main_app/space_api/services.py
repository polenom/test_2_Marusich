from dataclasses import dataclass

from django.contrib.auth.models import User


@dataclass
class UserDataClass:
    username: str
    email: str
    password: str = None

    @classmethod
    def from_instance(cls, user: "User") -> "UserDataClass":
        print(cls, cls.__class__.__name__)
        return cls(
            username=user.username,
            email=user.email
        )

def create_user(user_dc: "UserDataClass") -> "UserDataClass":
    instance = User(username=user_dc.username, email=user_dc.email)
    if user_dc.password is not None:
        instance.set_password(user_dc.password)
    instance.save()
    return UserDataClass.from_instance(instance)