from setuptools import setup, find_packages

install_requires = [
    'certifi==2020.12.5',
    'chardet==4.0.0',
    'greenlet==1.0.0',
    'idna==2.10',
    'importlib-metadata==3.10.1',
    'lxml==4.6.3',
    'psycopg2==2.8.6',
    'pymongo==3.11.3',
    'requests==2.25.1',
    'Sickle==0.7.0',
    'SQLAlchemy==1.4.7',
    'typing-extensions==3.7.4.3',
    'urllib3==1.26.4',
    'zipp==3.4.1']

setup(
    name='scielo-data',
    version='0.1',
    author="SciELO",
    author_email="scielo-dev@googlegroups.com",
    license="BSD",
    url="https://github.com/scieloorg/scielo-data",
    keywords='scholarly data disambiguation',
    maintainer_email='rafael.pezzuto@gmail.com',
    packages=find_packages(),
    install_requires=install_requires,
    entry_points="""
        [console_scripts]
        getter_initdb=getter.initialize_database:main
        getter_raw=getter.raw_getter:main
        """
)
