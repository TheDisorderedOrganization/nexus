from tqdm import tqdm
import numpy as np
import os

from .config.settings import Settings
from .io.reader.reader_factory import ReaderFactory
from .core.system import System
from .analysis.finder_factory import FinderFactory
from .analysis.analyzer_factory import AnalyzerFactory
from .io.writer.writer_factory import WriterFactory
from .utils import *

def main(settings: Settings):
    """
    Main function to test the package.
    """
    # Create export directory
    settings.export_directory = os.path.join(settings.export_directory, settings.project_name)
    if not os.path.exists(settings.export_directory):
        os.makedirs(settings.export_directory)

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
    for analyzer in settings.analysis.get_analyzers():
        analyzers.append(AnalyzerFactory(settings).get_analyzer(analyzer))

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

        if settings.clustering.with_printed_unwrapped_clusters:
            writer = WriterFactory(settings).get_writer('ClustersWriter')
            writer.set_clusters(frame.get_clusters())
            writer.write()

    # Print results
    for analyzer in analyzers:
        analyzer.print_to_file()              
        
        
    