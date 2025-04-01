from tqdm import tqdm
import numpy as np
import os

from .config.settings import Settings
from .io.reader.reader_factory import ReaderFactory
from .core.system import System
from .analysis.finder_factory import FinderFactory
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

    # Initialize analyzers
    analyzers = []
    frame_processed = []
    for analyzer in settings.analysis.get_analyzers():
        analyzers.append(AnalyzerFactory(frame_processed, verbose=settings.verbose).get_analyzer(analyzer))

    progress_bar_kwargs = {
            "disable": not settings.verbose,
            "leave": False,
            "ncols": os.get_terminal_size().columns,
            "colour": "red"
        }

    progress_bar = tqdm(enumerate(system.iter_frames()), desc="Processing frames ...", unit="frame", total=total+1, **progress_bar_kwargs)

    # Process frames
    for i, frame in progress_bar:
        j = i + settings.range_of_frames[0]
        progress_bar.set_description(f"Processing frame {j} of {settings.range_of_frames} frames...")
        if settings.lattice.apply_custom_lattice:
            frame.set_lattice(settings.lattice.custom_lattice)
        
        frame.initialize_nodes()
        finder = FinderFactory(frame, settings).get_finder(settings)
        finder.find_neighbors()
        clusters = finder.find_clusters()
        
        frame.set_clusters(clusters)

        for analyzer in analyzers:
            analyzer.analyze(frame)

    # Debug get results
    for analyzer in analyzers:
        print(analyzer.get_result())

    # Process results
    for analyzer in analyzers:
        analyzer.finalize()

    # Print results
    for analyzer in analyzers:
        analyzer.print_to_file()              
        
        
    