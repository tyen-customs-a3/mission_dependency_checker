from setuptools import setup, find_packages

setup(
    name="mission_checker",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
        ],
    }
)
