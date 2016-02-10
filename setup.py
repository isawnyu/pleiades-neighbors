from setuptools import setup, find_packages
import os

version = '0.2'

setup(name='pleiades.neighbors',
      version=version,
      description="views of a feature's bneighborhood",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='geography',
      author='Sean Gillies',
      author_email='sean.ggillies@gmail.com',
      url='http://svn.plone.org/svn/plone/plone.example',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['pleiades'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'collective.geo.geographer',
          # -*- Extra requirements: -*-
      ],
)
