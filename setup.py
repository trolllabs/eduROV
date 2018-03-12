# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
from edurov.support import detect_pi

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='edurov',  # Required
    version='0.0.1a1',  # Required
    description='A educational project for remotely operated vehicles',  # Required
    long_description=long_description,  # Optional
    url='https://github.com/trolllabs/eduROV',  # Optional
    author='trolllabs',  # Optional
    author_email='martinloland@gmail.com',  # Optional
    classifiers=[  # Optional
        # How mature is this project?
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Education',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Multimedia :: Video :: Display',
        'Framework :: Robot Framework',

        # Pick your license as you wish
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='video education ROV picamera',  # Optional
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),  # Required
    install_requires=['pygame', 'Pyro4']+(['picamera==1.13' if detect_pi() else []]),  # Optional
    python_requires='>=3',  # Optional
    package_data={  # Optional
        'edurov': ['index.html', 'keys.txt', 'static/script.js',
                   'static/style.css'],
    },
    entry_points={  # Optional
        'console_scripts': [
            'edurov-http = edurov.http:main',
        ],
    },
)
