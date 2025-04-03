from typing import Optional
from .base_writer import BaseWriter
from .clusters_writer import ClustersWriter
from ...config.settings import Settings

# TODO: finish implementation of writers 
#       - add support for trajectory writers
#       - add support for system writers
#       - add support for configuration writers
#       - add support for summary writers
#       - add support for statistics writers
#       - add support for performance writers


class WriterFactory:
    """Factory for creating file writers based on file type."""

    def __init__(self, settings: Settings):
        self._writers = {}
        self._settings: Settings = settings
        self.register_writer(ClustersWriter)

    
    def register_writer(self, writer: BaseWriter):
        """Registers a new writer instance."""
        self._writers[writer.__class__.__name__] = writer

    def get_writer(self, name: str) -> Optional[BaseWriter]:
        """Returns the appropriate writer for a given file."""
        if name == "ClustersWriter":
            return ClustersWriter(self._settings)
        else:
            return None