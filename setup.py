
from distutils.core import setup

classifiers = ['Development Status :: 5 - Production/Stable',
               'Operating System :: POSIX :: Linux',
               'License :: OSI Approved :: MIT License',
               'Intended Audience :: Developers',
               'Programming Language :: Python :: 2.7',
               'Topic :: Software Development',
               'Topic :: Home Automation',
               'Topic :: System :: Hardware']

setup(name             = 'grow-io',
      version          = '0.0.1',
      author           = 'Jorge Dias',
      author_email     = 'mar.ori@gmail.com',
      description      = 'grow-board basic IO module',
      long_description = open('README.txt').read(),
      license          = 'BSD',
      keywords         = 'hydroponics grow manager',
      url              = 'http://github.com/marori/grow-io/',
      classifiers      = classifiers,
      packages         = ['grow-io'])
