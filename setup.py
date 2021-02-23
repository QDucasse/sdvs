from setuptools import find_namespace_packages, setup

from sdvs import __version__, __name__

# Installation dependencies
install_requires = [
]

# Development dependencies
development_extras = [
    'flake8',
    'pytest',
    'pytest-cov',
    'tox',
]

setup(
    name=__name__,
    version=__version__,
    packages=find_namespace_packages(exclude=['tests']),
    include_package_data=True,
    license='MIT License (MIT)',
    description='',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/QDucasse/sdvs',
    author='Quentin Ducasse',
    author_email='quentin.ducasse@ensta-bretagne.org',
    install_requires=install_requires,
    extras_require={
        'development': development_extras,
    },
    classifiers=[
        # See https://pypi.org/classifiers/
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',

        # Typically you may include
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Environment :: Console',
        # 'Environment :: Web Environment',
        # 'Intended Audience :: Developers',
        # 'Intended Audience :: End Users/Desktop',
        # 'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        # 'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        # 'Topic :: Office/Business',
        # 'Topic :: Internet :: WWW/HTTP',
        # 'Topic :: Software Development',
    ],
)
