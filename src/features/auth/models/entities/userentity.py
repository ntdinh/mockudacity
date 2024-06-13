from __future__ import annotations

from dataclasses import dataclass
from sqlalchemy import Column, Boolean, String, SmallInteger
import bcrypt

from src.models.entities import BaseEntity


@dataclass
class UserEntity(BaseEntity):
    __tablename__ = 'Users'

    Username = Column(String(50), unique=True)
    HashedPasswd = Column(String(1000))
    Email = Column(String(250), unique=True)
    Name = Column(String(250))
    BirthDay = Column(String(250))
    Sex = Column(SmallInteger())
    Avatar = Column(String(1000))
    Activate = Column(Boolean())

    def __init__(self, **params):
        super().__init__(**params)

        if 'Username' in params:
            self.Username = params['Username']
        if 'Passwd' in params:
            passwdEncode = params['Passwd'].encode('utf-8')
            self.HashedPasswd = bcrypt.hashpw(passwdEncode, bcrypt.gensalt())
        if 'Email' in params:
            self.Email = params['Email']
        if 'Name' in params:
            self.Name = params['Name']
        if 'BirthDay' in params:
            self.BirthDay = params['BirthDay']
        if 'Sex' in params:
            self.Sex = params['Sex']
        if 'Avatar' in params:
            self.Avatar = params['Avatar']
        if 'Activate' in params:
            self.Activate = params['Activate']

    def copyFrom(self, entity: UserEntity):
        super().copyFrom(entity)

        if entity.Username is not None:
            self.Username = entity.Username
        if entity.HashedPasswd is not None:
            self.HashedPasswd = entity.HashedPasswd
        if entity.Email is not None:
            self.Email = entity.Email
        if entity.Name is not None:
            self.Name = entity.Name
        if entity.BirthDay is not None:
            self.BirthDay = entity.BirthDay
        if entity.Sex is not None:
            self.Sex = entity.Sex
        if entity.Avatar is not None:
            self.Avatar = entity.Avatar
        if entity.Activate is not None:
            self.Activate = entity.Activate

    def verifyPasswd(self, passwd: str) -> bool:
        passwdEncode = passwd.encode('utf-8')
        hashedPasswdEncode = self.HashedPasswd.encode('utf-8')
        return bcrypt.checkpw(passwdEncode, hashedPasswdEncode)
