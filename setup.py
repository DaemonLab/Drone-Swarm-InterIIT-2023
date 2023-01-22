from setuptools import setup

setup(
    name='pypluto',
    version='0.0.1',
    packages=['pypluto'],
    url='https://github.com/DaemonLab/Drone-Swarm',
    license='Open Source',
    description='This API to connect Pluto Drone',
    install_requires= [
        'python>=3.7',
        'numpy==1.17.4',
        'opencv_contrib_python==4.6.0.66',
        'setuptools==45.2.0'
    ]
)
