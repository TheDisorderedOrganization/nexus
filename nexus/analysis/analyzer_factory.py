from typing import Optional, List
from ..core.frame import Frame
from .base_analyzer import BaseAnalyzer
from .average_cluster_size_analyzer import AverageClusterSizeAnalyzer
from .largest_cluster_size_analyzer import LargestClusterSizeAnalyzer
from .spanning_cluster_size_analyzer import SpanningClusterSizeAnalyzer
from .percolation_probability_analyzer import PercolationProbabilityAnalyzer
from .order_parameter_analyzer import OrderParameterAnalyzer
from .cluster_size_distribution_analyzer import ClusterSizeDistributionAnalyzer
from .gyration_radius_analyzer import GyrationRadiusAnalyzer
from .correlation_length_analyzer import CorrelationLengthAnalyzer

class AnalyzerFactory:
    def __init__(self, frame_processed: List[Frame], verbose: bool = True):
        self._analyzers = {}
        # Register other analyzers here
        self.register_analyzer(AverageClusterSizeAnalyzer(frame_processed, verbose))
        self.register_analyzer(LargestClusterSizeAnalyzer(frame_processed, verbose))
        self.register_analyzer(SpanningClusterSizeAnalyzer(frame_processed, verbose))
        self.register_analyzer(PercolationProbabilityAnalyzer(frame_processed, verbose))
        self.register_analyzer(OrderParameterAnalyzer(frame_processed, verbose))
        self.register_analyzer(ClusterSizeDistributionAnalyzer(frame_processed, verbose))
        self.register_analyzer(GyrationRadiusAnalyzer(frame_processed, verbose))
        self.register_analyzer(CorrelationLengthAnalyzer(frame_processed, verbose))

    def register_analyzer(self, analyzer: BaseAnalyzer) -> None:
        self._analyzers[analyzer.__class__.__name__] = analyzer

    def get_analyzer(self, analyzer_name: str) -> Optional[BaseAnalyzer]:
        return self._analyzers.get(analyzer_name)