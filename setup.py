from setuptools import find_packages
from distutils.core import setup

setup(name='acfile',
      version='0.3',
      description='File format allowing math operations, variables, and sections.',
      author='ArztKlein',
      author_email='',
      url='https://github.com/ArztKlein/acf',
      keywords=['file','format', 'configuration', 'filetype'],
      setup_requires=['wheel'],
      python_requires='>3.6.1',
      packages=find_packages(),
      include_package_data=True,
      install_requires=[
            'sly'
      ]
)