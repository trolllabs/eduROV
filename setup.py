# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
from edurov.support import detect_pi

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='edurov',
    version='0.0.1a4',
    description='A educational project for remotely operated vehicles',
    long_description=long_description,
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
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=[
         'pygame',
         'Pyro4']+
         (['picamera==1.13' if detect_pi() else []]),
    python_requires='>=3',
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'edurov-http = edurov.http:main',
        ],
    },
)
