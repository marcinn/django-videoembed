from setuptools import setup, find_packages

setup(
    name='django-videoembed',
    version='0.2',
    description="Easy embedding videos with Django",
    author='Marcin Nowak',
    author_email='marcin.j.nowak@gmail.com',
    url='https://github.com/marcinn/django-video-embed',
    packages=find_packages(),
    package_dir={'videoembed': 'videoembed'},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    zip_safe=False,
    include_package_data=True,
)
