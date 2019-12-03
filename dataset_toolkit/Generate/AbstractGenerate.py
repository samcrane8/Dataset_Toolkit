from abc import ABC, abstractmethod


class AbstractGenerate(ABC):

    @abstractmethod
    def generate(self, img) -> list:
        pass
