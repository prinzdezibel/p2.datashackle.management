from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='p2.datashackle.management',
      version=version,
      description="",
      #long_description=open("README.txt").read() + "\n" +
      #                 open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='projekt und partner',
      author_email='mail@projekt-und-partner.de',
      url='http://datashackle.net',
      license='GPL',
      packages=find_packages(),
      namespace_packages=['p2', 'p2.datashackle'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points={
          'fanstatic.libraries': [
              'foobar = p2.datashackle.management:management_library',
               ],
      }
      )
