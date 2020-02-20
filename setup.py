from setuptools import setup

setup(
    name='find_store',
    version='0.0.1',
    description='',
    author='Olena Marushchenko',
    author_email='markohelen@gmail.com',
    entry_points={
        'console_scripts': [
            'find_store=store.main:main'
        ]
    },
    packages=[
    	'store'
    ],
    install_requires=[
    	'googlemaps'
    ],
    include_package_data=True,
    data_files = [('', ['store/data/store-locations.csv'])],
    package_data={'store/data': ['data/*.csv']},
)