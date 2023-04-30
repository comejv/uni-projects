from setuptools import setup, Extension

csat = Extension('Csat', sources=['libsat.c'],
                 extra_compile_args=["-O3"])

setup(
    name='Csat',
    version='0.1',
    description='C walksat solver',
    ext_modules=[csat]
)
