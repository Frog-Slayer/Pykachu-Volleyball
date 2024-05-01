from setuptools import setup, find_packages

setup(
    name='Pykachu Volleyball',
    version='0.0.1',
    description='A single-agent reinforcement learning environment of the game Pikachu Volleyball, using gymnasium',
    author='frog-slayer',
    author_email='pj0642@gmail.com',
    url='https://github.com/Frog-Slayer/Pykachu-Volleyball',
    install_requires=['gymnasium', 'pygame'],
    packages=find_packages(exclude=[]),
    keywords=['pikachu', 'volleyball', 'gym', 'pykachu', 'gymnasium'],
    python_requires='>=3.8',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
