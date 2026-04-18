from setuptools import setup

package_name = 'lost_book_bridge'

setup(
    name=package_name,
    version='0.0.1',
    py_modules=['bridge'],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/lost_book_bridge']),
        ('share/lost_book_bridge', ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    entry_points={
        'console_scripts': [
            'bridge = bridge:main',
        ],
    },
)
