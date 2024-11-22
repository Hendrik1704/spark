from setuptools import find_packages, setup

setup(
    name='sparkx',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        "particle==0.23.0",
        "numpy>=1.23.5",
        "scipy>=1.10.1",
        "abc-property==1.0",
        "fastjet>=3.4.2.1",
        "matplotlib>=3.7.1",
    ],
    version='2.0.0',
    description='Software Package for Analyzing Relativistic Kinematics in Collision eXperiments',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author='Niklas Götz, Renata Krupczak, Hendrik Roch, Nils Sass',
    author_email="goetz@itp.uni-frankfurt.de, hroch@wayne.edu, nsass@itp.uni-frankfurt.de",
    url="https://smash-transport.github.io/sparkx/",
    download_url="https://github.com/smash-transport/sparkx",
    license='GNU General Public License v3.0',
    include_package_data = True
)
