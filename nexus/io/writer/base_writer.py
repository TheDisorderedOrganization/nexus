from abc import ABC, abstractmethod

class BaseWriter(ABC):
    """
    Abstract base class for results writers. Defines the common interface.
    """

    verbose: bool = True

    def set_verbose(self, verbose: bool) -> None:
        self.verbose = verbose

    @abstractmethod
    def write(self, filepath: str) -> None:
        pass

    # TODO: finish implementation of writers 
    #       - add support for results writers
    #       - add support for trajectory writers
    #       - add support for system writers
    #       - add support for configuration writers
    #       - add support for summary writers
    #       - add support for statistics writers
    #       - add support for performance writers