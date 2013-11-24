# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

install_requires = [
    'Django >= 1.3',
    'django-crispy-forms',
    'django-simple-captcha'
]

setup(
    name='django-ineo',
    version=get_captcha_version(),
    description='Simple comments for any model. Comments supported response with 2-level hierarchy.',
    long_description = open('README.rst').read(),
    keywords='comments, django',
    author='Ivan Morgun',
    author_email='i@proft.me',
    url='https://github.com/proft/django-ineo',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Framework :: Django',
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires
)
