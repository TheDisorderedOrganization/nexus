from abc import ABC, abstractmethod
from typing import List, Dict

from ...core.frame import Frame   
from ...config.settings import Settings

class BaseAnalyzer(ABC):
    """
    Abstract base class for all analyzers in the Nexus framework.
    
    This class defines the common interface that all analyzer implementations must follow.
    Analyzers are responsible for processing Frame objects, extracting relevant information,
    and producing analysis results that can be retrieved or written to output files.
    
    Attributes:
        frame_processed (List[Frame]): List of frames that have been processed by the analyzer.
        _settings (Settings): Configuration settings for the analyzer.
    """
    def __init__(self, settings: Settings) -> None:
        """
        Initialize the BaseAnalyzer with settings.
        
        Args:
            settings (Settings): Configuration settings for the analyzer.
        """
        self.frame_processed: List[Frame] = []
        self._settings: Settings = settings

    @abstractmethod
    def analyze(self, frame: Frame) -> None:
        """
        Analyze a single frame.
        
        This method should implement the specific analysis logic for the derived analyzer.
        
        Args:
            frame (Frame): The frame to analyze.
        """
        pass

    @abstractmethod
    def update_frame_processed(self, frame: Frame) -> None:
        """
        Update the list of processed frames.
        
        This method should be called after a frame has been analyzed to keep track
        of processed frames.
        
        Args:
            frame (Frame): The frame that has been processed.
        """
        pass

    @abstractmethod
    def finalize(self) -> None:
        """
        Finalize the analysis after all frames have been processed.
        
        This method should perform any post-processing steps needed after
        all frames have been analyzed, such as calculating averages or
        other aggregate statistics.
        
        Returns:
            Any: The final analysis results.
        """
        pass

    @abstractmethod
    def get_result(self) -> Dict[str, float]:
        """
        Get the current analysis results.
        
        This method should return the current state of the analysis results,
        typically after finalize() has been called.
        
        Returns:
            Dict[str, float]: A dictionary containing analysis results.
        """
        pass

    @abstractmethod
    def print_to_file(self) -> None:
        """
        Write the analysis results to a file.
        
        This method should handle writing the analysis results to an output file,
        with appropriate formatting and headers.
        """
        pass

    def __str__(self) -> str:
        """
        Return a string representation of the analyzer.
        
        Returns:
            str: The name of the analyzer class.
        """
        return f"{self.__class__.__name__}"

    def __repr__(self) -> str:
        """
        Return a string representation for debugging.
        
        Returns:
            str: A string representation that could be used to recreate the analyzer.
        """
        return f"{self.__class__.__name__}()"