from setuptools import setup, find_packages
from addonpy.addonpyHelpers import AddonHelper

version = AddonHelper.get_version()

EXCLUDE_FROM_PACKAGES = ['addonpy.docs',
                         'addonpy.scripts']

setup(
    name='addonpy',
    version=version,
    url='https://github.com/ninadmhatre/addonpy/wiki',
    author='Ninad Mhatre',
    author_email='ninad.mhatre@gmail.com',
    description='A simple addon/plug-in module',
    license='MIT',
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    package_data={'': ['*.version', '*.conf' '*.info']},
    data_files=[
        ('addonpy', ['.version'])
    ],
    scripts=['addonpy/scripts/addon_generator.py'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)