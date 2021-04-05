from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

with open('CHANGELOG.md', 'r', encoding='utf-8') as f:
    long_description = long_description + '\n\n' + f.read()

setup(
    name='pynumethods',
    version='0.1.1',
    author='NJL',
    author_email='njl.takode@gmail.com',
    description='Using various methods to find for the approximate root of function',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/notjl/pynumethods',
    project_urls={
        'Bug Tracker': 'https://github.com/notjl/pynumethods/issues',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Intended Audience :: Education',
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    license='MIT',
    keywords=[
        'numerical methods',
        'calculator',
    ],
    install_requires=[
        'sympy>=1.7.1'
    ]
)