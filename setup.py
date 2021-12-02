from setuptools import setup, find_packages

install_requires = [
    'certifi==2021.5.30',
    'charset-normalizer==2.0.4',
    'idna==3.2',
    'lxml==4.6.3',
    'pymongo==3.12.0',
    'requests==2.26.0',
    'Sickle==0.7.0',
    'urllib3==1.26.6',
    'xmltodict==0.12.0']

setup(
    name='scielo-nw',
    version='0.2.3',
    author="SciELO",
    author_email="scielo-dev@googlegroups.com",
    license="BSD",
    url="https://github.com/scieloorg/scielo-nw",
    keywords='scholarly data gather',
    maintainer_email='rafael.pezzuto@gmail.com',
    packages=find_packages(),
    install_requires=install_requires,
    entry_points="""
        [console_scripts]
        getter=getter.raw_getter:main
        """
)
