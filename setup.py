from setuptools import setup, find_packages
import os

# Read the long description from README
long_description = ""
if os.path.exists("README.md"):
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()

setup(
    name='gaybeck-starkids-sms',
    version='2.0.0',
    description='Comprehensive School Management System with Fee Management, Attendance Tracking, and Financial Reports',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Gaybeck Starkids School',
    author_email='info@gaybeckstarkids.edu.gh',
    url='https://github.com/Ashgabb/gaybeck-starkids-sms',
    py_modules=['sms', 'uninstall', 'post_install'],
    packages=find_packages(exclude=['tests', 'tests.*', 'docs', 'backups', 'dev-scripts']),
    include_package_data=True,
    package_data={
        '': ['database/*.db', 'database/.gitkeep', 'teacher_documents/*', 'reports/*', '*.py', '*.ico'],
    },
    data_files=[
        ('', ['icon.ico']),  # Install icon in package root
        ('database', []),  # Ensure database directory is created
        ('teacher_documents', []),  # Ensure teacher_documents directory is created
        ('reports', []),  # Ensure reports directory is created
    ],
    install_requires=[
        'tkcalendar>=1.6.1',
        'Pillow>=10.0.0',
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'black>=22.0.0',
            'flake8>=4.0.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'starkids-sms=sms:start_application',
            'starkids-sms-uninstall=uninstall:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'Topic :: Education',
        'Topic :: Office/Business',
    ],
    python_requires='>=3.8',
    keywords='school management student attendance fees finance education',
    project_urls={
        'Bug Reports': 'https://github.com/Ashgabb/gaybeck-starkids-sms/issues',
        'Source': 'https://github.com/Ashgabb/gaybeck-starkids-sms',
        'Documentation': 'https://github.com/Ashgabb/gaybeck-starkids-sms/tree/main/docs',
    },
)
