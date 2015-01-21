from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'SQLAlchemy',
    'cryptacular',
    'pyramid',
    'pyramid_debugtoolbar',
    'pyramid_jinja2',
    'pyramid_tm',
    'transaction',
    'waitress',
    'wtforms',
    'zope.sqlalchemy',
]

setup(
    name='learning_journal',
    version='0.1',
    description='learning_journal',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author='Salim Hamed',
    author_email='salimhamed@gmail.com',
    url='',
    keywords='web wsgi bfg pylons pyramid',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite='learning_journal',
    install_requires=requires,
    # entry points are ways we can run our code once installed
    entry_points="""\
    [paste.app_factory]
    main = learning_journal:main
    [console_scripts]
    initialize_learning_journal_db = learning_journal.scripts.initializedb:main
    """,
)
