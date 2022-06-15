from abc import ABC, abstractmethod

class AbstractClass(ABC):
    def accept(self):
        pass
    def label(self):
        pass
    def normalize(self):
        pass

class SpellClass(AbstractClass):
    def __init__(self):
        super().__init__()
        self.class_name = 'spell'

    def accept(self, token):
        if (token.isalpha()):
            return True
        else:
            return False
    def label(self, token_norm, token_unnorm):
        if  self.accept(token_unnorm):
            count_space = token_norm.count(" ")
            if (len(token_unnorm)-1 == count_space):
                temp = token_norm.split(" ")
                for i in range(len(temp)):
                    if (len(temp[i])!=1 or temp[i] != token_unnorm.lower()[i]):
                        return False
                return True
            return False
        else:
            return False