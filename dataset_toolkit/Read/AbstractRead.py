from ABC import ABC


class AbstractRead(ABC):

    def read(self, path: str) -> list:
        pass
