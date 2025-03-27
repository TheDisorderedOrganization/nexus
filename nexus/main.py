from tqdm import tqdm
import numpy as np
import os

from .config.settings import Settings
from .io.reader.reader_factory import ReaderFactory
from .core.system import System
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

    progress_bar = tqdm(enumerate(system.iter_frames()), total=total, desc="Parsing frames", unit="frame", **progress_bar_kwargs)
    for i, frame in progress_bar:
        if settings.lattice.apply_custom_lattice:
            frame.set_lattice(settings.lattice.custom_lattice)
        
        frame.initialize_nodes()
        nodes = frame.nodes
        print(nodes)


    