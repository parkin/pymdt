from distutils.core import setup

## Read the version string
import re
VERSIONFILE="pymdt/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

setup(name='pymdt',
    version=verstr,
    description='Reads some NT-MDT files',
    author='Will Parkin',
    author_email='wmparkin@gmail.com',
    url='https://github.com/parkin/pymdt',
    packages=['pymdt']
    )
