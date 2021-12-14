import setuptools
#from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
      name='hexahackathon',
      version='0.0.1',
      description='analyze participant contributions for code reviews',
      long_description=long_description,
      long_description_content_type="text/markdown",
      package_dir={'':'src'},
      classifiers=[
          "Programming Language :: Python :: 3.7",
           "Operating System :: OS Independent",
          ],
      packages=setuptools.find_packages(where="src"),
      )