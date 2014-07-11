from setuptools import setup, find_packages

setup(
    name='addonpy',
    version='0.6.0',
    author='Ninad Mhatre',
    author_email='ninad.mhatre@gmail.com',
    packages=['addonpy', 'addonpy.tests', 'addonpy.examples', 'addonpy.docs', 
              'addonpy.examples.Default', 'addonpy.examples.Default.Hook'],
    package_data = {'addonpy.tests': ['*.bat', '*.txt'],
                    'addonpy.examples': ['*.txt', '*.info'],
                    'addonpy.docs': ['*.html']},
    url='https://github.com/ninadmhatre/addonpy/wiki',
    license='MIT',
    description='A simple addon/plug-in module',
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)