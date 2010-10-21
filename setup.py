from setuptools import setup, find_packages
import codecs

setup(name='pyPostal',
      maintainer='Maximillian Dornseif',
      maintainer_email='md@hudora.de',
      url='http://github.com/hudora/pyPostal/#readme',
      version='1.1b',
      description='pyPostal is an Interface for sending real (paper-based) letters via API (Pixelletter)',
      long_description=codecs.open('README.rst', "r", "utf-8").read(),
      license='BSD',
      classifiers=['Intended Audience :: Developers',
                   'Programming Language :: Python'],
      packages = find_packages(),
      zip_safe = False,
      )
