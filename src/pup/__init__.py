"""
Pluggable Micro Packager
"""

__version__ = '1.0.0a17'

__title__ = 'pup'
__description__ = 'Pluggable Micro Packager'

__license__ = 'MIT'
__uri__ = 'https://github.com/mu-editor/pup/'

__author__ = 'Tiago Montes'
__email__ = 'tiago.montes@gmail.com'



from . api import package

__all__ = ['package']
