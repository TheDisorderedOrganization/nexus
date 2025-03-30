from typing import Optional, List
from .base_finder import BaseFinder

class FinderFactory:
    def __init__(self, frame: Frame, settings: Settings) -> None:
        self._finders = {}
        # Register other finders here
        self.register_finder(ClusterFinder(frame, settings))

    def register_finder(self, finder: BaseFinder) -> None:
        self._finders[finder.__class__.__name__] = finder

    def get_finder(self, finder_name: str) -> Optional[BaseFinder]:
        return self._finders.get(finder_name)