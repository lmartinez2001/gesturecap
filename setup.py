from setuptools import setup, find_packages

setup(
    name='GestureCap',
    version='0.1',
    packages=find_packages(),
    description="GSoC project",
    extras_require={
        'flir': ['dependencies/spinnaker_python-4.0.0.116-cp310-cp310-linux_x86_64.whl']
    },
)
