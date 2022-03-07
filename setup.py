from setuptools import setup

setup(
    name='calculations',
    version='2.0.0',
    packages=[
        'spectrum',
        'spectrum.gui',
        'spectrum.gui.graph',
        'spectrum.graph',
        'spectrum.tools',
        'spectrum.modules',
        'spectrum.calculations',
        'spectrum.calculations.spectra'
    ],
    package_dir={'': 'src'},
    url='https://github.com/nskeip/calculations',
    license='Apache 2',
    author='Daniel Lytkin',
    maintainer='Nikita Hismatov',
    maintainer_email='me@ns-keip.ru',
    description=''
)
