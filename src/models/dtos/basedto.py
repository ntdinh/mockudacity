from ..entities import BaseEntity


class BaseDto(object):
    def __init__(self, baseEntity: BaseEntity):
        self.Code = baseEntity.Code
        self.CreatedAt = baseEntity.CreatedAt
        self.ModifiedAt = baseEntity.ModifiedAt

    def toDict(self) -> dict:
        return {
            'Code': self.Code,
            'CreatedAt': self.CreatedAt,
            'ModifiedAt': self.ModifiedAt
        }
