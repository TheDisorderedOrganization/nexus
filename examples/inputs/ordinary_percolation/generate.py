# This script generate percolation sites in a 100x100x100 orthohombic lattice

import numpy as np
from numba import jit
from typing import List

@jit(nopython=True, cache=True, fastmath=True)
def generate_sites(probability: float) -> List[str]:
    sites = []
    for i in range(30):
        for j in range(30):
            for k in range(30):
                this_probability = np.random.random()
                # generate the lattice position of the sites
                x = i % 30
                y = j % 30
                z = k % 30

                if this_probability < probability:
                    sites.append(f"1 {x} {y} {z}")
                else:
                    continue    

    return sites

if __name__ == "__main__":
    for i in range(1,41):
        probability = (i * 0.025)
        sites = generate_sites(probability)
        with open(f"percolation_sites_{probability:.3f}.xyz", "w") as f:
            f.write(f"{len(sites)}\n")
            f.write("Lattice=\"30.0 0.0 0.0 0.0 30.0 0.0 0.0 0.0 30.0\"\n")
            for site in sites:
                f.write(site + "\n")
        f.close()

        