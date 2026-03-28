from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'litho_brain'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'assets'), glob('litho_brain/assets/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='zeyadcode',
    maintainer_email='zeyadshapan2004@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'litho_brain = litho_brain.brain_node:main',
            'autofocus_node = litho_brain.nodes.autofocus_node:main',
            'autoalignment_node = litho_brain.nodes.autoalignment_node:main',
        ],
    },
)
