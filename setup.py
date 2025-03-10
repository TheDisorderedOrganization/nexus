from setuptools import setup, find_packages

setup(
    name="nexus-cat",
    version="1.0.4",
    description="Nexus is a Cluster Analysing Toolkit package for atomic systems.",
    author="Julien Perradin",
    author_email="julien.perradin@protonmail.fr",
    url="https://github.com/jperradin/nexus",
    packages=find_packages(),
    install_requires=["numpy", "scipy", "tqdm", "natsort", "colorama"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Visualization",
        "Operating System :: OS Independent",
    ],
    project_description=open("README.md").read(),
)
