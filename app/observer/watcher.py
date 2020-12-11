from abc import abstractmethod, abstractproperty, ABC


class Watcher(ABC):
    """Abstract Observers implementation """
    def __init__(self):
        self._data = None
    
    @abstractmethod
    def retrieve(self, date: str) -> None:
        """Retrieves info from source"""
        pass

    @abstractmethod
    def update_database(self) -> None:
        """Updates database with observed information"""
        pass
