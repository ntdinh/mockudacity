from src.models.dtos import BaseDto

from ..entities import UserEntity


class UserDto(BaseDto):
    def __init__(self, userEntity: UserEntity):
        super().__init__(userEntity)

        self.Username = userEntity.Username
        self.Email = userEntity.Email
        self.Name = userEntity.Name
        self.BirthDay = userEntity.BirthDay
        self.Sex = userEntity.Sex
        self.Avatar = userEntity.Avatar
        self.Activate = userEntity.Activate
        self.Token = None

    def toDict(self) -> dict:
        return {
            **super().toDict(),
            'Username': self.Username,
            'Email': self.Email,
            'Name': self.Name,
            'BirthDay': self.BirthDay,
            'Sex': self.Sex,
            'Avatar': self.Avatar,
            'Activate': self.Activate,
            'Token': self.Token
        }
