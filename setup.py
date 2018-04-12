import os
import sys

from setuptools import setup, find_packages

from edurov.utils import detect_pi

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 0)

if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write(
        """
        ==========================
        Unsupported Python version
        ==========================
        
        eduROV requires python 3, try using pip3 instead of pip.
        """)
    sys.exit(1)


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='edurov',
    version='0.0.4',
    description='A educational project for remotely operated vehicles',
    long_description=read('README.rst'),
    license='GPLv3',
    url='https://github.com/trolllabs/eduROV',

    author='trolllabs',
    author_email='martinloland@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Education',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Multimedia :: Video :: Display',
        'Framework :: Robot Framework',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    keywords='video education ROV picamera',
    install_requires=[
                         'Pyro4'] +
                     (['picamera==1.13' if detect_pi() else []]),
    python_requires='>=3',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'edurov-web = examples_edurov.entry_points:edurov_web',
            'edurov-duo = examples_edurov.entry_points:edurov_duo',
            'edurov-min = examples_edurov.entry_points:edurov_min'
        ],
    },
    project_urls={
        'Documentation': 'http://http://edurov.no/',
        'Source': 'https://github.com/trolllabs/eduROV/',
        'Tracker': 'https://github.com/trolllabs/eduROV/issues',
    }
)
