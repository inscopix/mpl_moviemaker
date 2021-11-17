from setuptools import setup

setup(
    name='mpl_moviemaker',
    version='0.0.1',
    packages=['mpl_moviemaker'],
    include_package_data=True,
    description='Wrapper for the Matplotlib Animation class that facilitates movie generation',
    url='https://github.com/inscopix/mpl_moviemaker',
    author='Inscopix',
    author_email='dollerenshaw@inscopix.com',
    install_requires=[
        'pandas',
        'seaborn',
        'matplotlib',
        'numpy',
        'tqdm',
        'ipykernel',
    ],
)