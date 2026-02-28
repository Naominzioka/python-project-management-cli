from abc import ABC, abstractmethod
#inheritance class for user to inherit from and any other person we may add in future.
class Person(ABC):
    def __init__(self, name, email):
        self.name = name
        self.email = email

    @abstractmethod
    def to_dict(self):
        pass
    

       