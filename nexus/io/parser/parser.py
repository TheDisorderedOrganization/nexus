from typing import List
from nexus.config.settings import Settings

import os

class Parser:
    def __init__(self, file_location: str, parser: str, settings: Settings):
        self.file_location: str = file_location
        self.parser: str = parser
        self._settings: Settings = settings
        self._files: List[str] = []
        self._infos: List[str] = [] # implement later

    def parse(self) -> List[str]:
        # checktype of file_location
        if os.path.exists(self.file_location):
            if os.path.isfile(self.file_location):
                # take parent directory instead
                parent_directory = os.path.dirname(self.file_location)
                if self._settings.verbose:
                    print(f"Parsing file: {parent_directory}")
                files = []
                for root, dirs, files in os.walk(parent_directory):
                    for file in files:
                        if file.endswith(".xyz"):
                            files.append(os.path.join(root, file))
                files.sort()
                self._files = files
                return files
            elif os.path.isdir(self.file_location):
                if self._settings.verbose:
                    print(f"Parsing directory: {self.file_location}")
                files = []
                for root, dirs, files in os.walk(self.file_location):
                    for file in files:
                        if file.endswith(".xyz"):
                            files.append(os.path.join(root, file))
                files.sort()
                self._files = files
                return files
            else:
                raise ValueError(f"File location {self.file_location} is not a directory")
        else:
            raise ValueError(f"File location {self.file_location} does not exist")
            
                    
                        
                
        