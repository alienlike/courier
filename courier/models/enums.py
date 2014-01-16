class Enum:
    def __init__(self, value):
        self.__validate()
        self.validate(value)
        self.__val = value

    def __int__(self):
        return self.__val

    @classmethod
    def __validate(cls):
        # ensure that the enum itself is valid
        for k in cls.__dict__.keys():
            if not k.startswith('__'):
                int(cls.__dict__[k])

    @classmethod
    def validate(cls, value):
        # check that a value is valid for the current enum
        for k in cls.__dict__.keys():
            if not k.startswith('__'):
                if cls.__dict__[k] == value:
                    return True
        raise ValueError

class AccountType(Enum):

    Person = 1
    System = 2
    Organization = 3
    Division = 4

class RouteType(Enum):

    Link = 1
    Group = 2
    Feed = 3
    List = 4

class LinkState(Enum):

    Pending = 1
    Accepted = 2
    Deferred = 3
    Broken = 4

class RecipientType(Enum):

    From = 1
    To = 2
    CC = 3
    BCC = 4

class FromTo(Enum):

    From = 1
    To = 2