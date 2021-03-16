from setuptools import setup

setup(
    name='reporter_app',
    packages=['reporter_app'],
    setup_requires=['libsass >= 0.6.0'],
    sass_manifests={
        'reporter_app': ('static/scss/', 'static/css', '/static/css')
    },
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)
