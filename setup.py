from setuptools import setup, find_packages



setup(name='gett',
        version='0.1',
        description='Genotype, expression, and trait toolset',
        author='Pablo Cordero',
        author_email='dimenwarper@gmail.com',
        url='https://github.com/dimenwarper/gett',
        packages = ['gett'] + ['gett.%s' % mod for mod in find_packages('gett')],
        install_requires=['numpy', 'scipy', 'rpy2', 'scikit-learn', 'networkx', 'matplotlib']
        )
