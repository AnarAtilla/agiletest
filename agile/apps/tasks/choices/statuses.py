from enum import Enum


class Statuses(Enum):
    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    PENDING = "PENDING"
    BLOCKED = "BLOCKED"
    TESTING = "TESTING"
    CLOSED = "CLOSED"

    @classmethod
    def choices(cls):
        return [(attr.value, attr.name.capitalize()) for attr in cls]