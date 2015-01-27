from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='pypstools',
      version='0.0.0.a',
      description='Python power system library',
      url='http://github.com/markwmuller/pypstools',
      author='Juan Manuel Mauricio',
      author_email='jmmauricio6@gmail.com',
      license='GPL V3',
      packages=['controlpy'],
      zip_safe=False,
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2.7',
        ],
      keywords='power system control small signal restructuredtext',
      )
