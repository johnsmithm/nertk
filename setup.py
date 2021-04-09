from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='nertk',
      version='0.0.2',
      description='Name Entity Recognition toolkit - Annotate name entities in text inline within your Jupyter notebook',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='http://github.com/johnsmithm/nertk',
      author='Ion Mosnoi',
      author_email='moshnoi2000@gmail.com',
      license='MIT',
      packages=['nertk'],
      install_requires=[
           'ipywidgets'
      ],      
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)