from tqdm import tqdm
import numpy as np
import os

from .config.settings import Settings
from .io.reader.reader_factory import ReaderFactory
from .core.system import System
from .analysis.clusters_finder import ClusterFinder
from .analysis.analyzer_factory import AnalyzerFactory
from .utils import *

def main(settings: Settings):
    """
    Main function to test the package.
    """

    if settings.verbose:
        print(settings)
    reader = ReaderFactory().get_reader(settings.file_location)
    reader.set_verbose(settings.verbose)

    system = System(reader, settings)

    if settings.range_of_frames[1] == -1:
        total = system.get_num_frames()
    else:
        total = settings.range_of_frames[1] - settings.range_of_frames[0]

    progress_bar_kwargs = {
        "disable": not settings.verbose,
        "leave": True,
        "ncols": os.get_terminal_size().columns,
        "colour": "green"
    }

    # Initialize analyzers
    analyzers = []
    for analyzer in settings.analysis.get_analyzers():
        analyzers.append(AnalyzerFactory(frame_processed=[], verbose=settings.verbose).get_analyzer(analyzer))

    print(analyzers)

    progress_bar = tqdm(enumerate(system.iter_frames()), total=total, desc="Parsing frames", unit="frame", **progress_bar_kwargs)
    for i, frame in progress_bar:
        if settings.lattice.apply_custom_lattice:
            frame.set_lattice(settings.lattice.custom_lattice)
        
        frame.initialize_nodes()
        cluster_finder = ClusterFinder(frame, settings)
        cluster_finder.find_neighbors()


    