from typing import Optional
from .base_writer import BaseWriter

# TODO: finish implementation of writers 
#       - add support for results writers
#       - add support for trajectory writers
#       - add support for system writers
#       - add support for configuration writers
#       - add support for summary writers
#       - add support for statistics writers
#       - add support for performance writers


class WriterFactory:
    """Factory for creating file writers based on file type."""

    def __init__(self):
        self._writers = {}

    def register_writer(self, writer: BaseWriter):
        """Registers a new writer instance."""
        # Use a dummy filename with the correct extension to determine support
        for ext in ['.dump']: #add your extensions here.
            if writer.supports_file_format(f'dummy{ext}'):
                self._writers[ext] = writer
                break

    def get_writer(self, filename: str) -> Optional[BaseWriter]:
        """Returns the appropriate writer for a given file."""
        for extension, writer in self._writers.items():
            if writer.supports_file_format(filename):
                return writer