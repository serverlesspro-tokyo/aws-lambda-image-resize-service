""":mod:`wand.cdefs.pixel_wand` --- Pixel-Wand definitions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. versionadded:: 0.5.0
"""
from ctypes import (CDLL, POINTER, c_char_p, c_double,
                    c_float, c_int, c_longdouble, c_size_t,
                    c_ubyte, c_uint, c_ushort, c_void_p)
from wand.cdefs.wandtypes import c_magick_char_p
import numbers

__all__ = ('load',)


def load(lib, IM_VERSION, IM_QUANTUM_DEPTH, IM_HDRI):
    """Define Pixel Wand methods. The ImageMagick version is given as
    a second argument for comparison. This will quick to determine which
    methods are available from the library, and can be implemented as::

        if IM_VERSION < 0x700:
            # ... do ImageMagick-6 methods ...
        else
            # ... do ImageMagick-7 methods ...

    .. seealso::

        #include "wand/pixel-wand.h"
        // Or
        #include "MagickWand/pixel-wand.h"

    Mapping Pixel methods also requires the wand library to evaluate
    what "Quantum" is to ImageMagick. We must query the library
    to identify if HRDI is enabled, and what the quantum depth is.

    .. seealso::

        MagickCore/magick-type.h

    :param lib: the loaded ``MagickWand`` library.
    :type lib: :class:`ctypes.CDLL`
    :param IM_VERSION: the ImageMagick version number (i.e. 0x0689).
    :type IM_VERSION: :class:`numbers.Integral`
    :param IM_QUANTUM_DEPTH: the ImageMagick Quantum Depth
                             (must be 8, 16, 32, or 64).
    :type IM_QUANTUM_DEPTH: :class:`numbers.Integral`
    :param IM_HDRI: if ImageMagick was compiled with HDRI support.
    :type IM_HDRI: :class:`bool`

    .. versionadded:: 0.5.0

    """
    if not isinstance(lib, CDLL):
        raise AttributeError(repr(lib) + " is not an instanced of ctypes.CDLL")
    if not isinstance(IM_VERSION, numbers.Integral):
        raise AttributeError("Expecting MagickCore version number")
    if IM_QUANTUM_DEPTH not in [8, 16, 32, 65]:
        raise AttributeError("QUANTUM_DEPTH must be one of 8, 16, 32, or 64")
    is_im_6 = IM_VERSION < 0x700
    is_im_7 = IM_VERSION >= 0x700

    if IM_QUANTUM_DEPTH == 8:
        QuantumType = c_float if IM_HDRI else c_ubyte
    elif IM_QUANTUM_DEPTH == 16:
        QuantumType = c_float if IM_HDRI else c_ushort
    elif IM_QUANTUM_DEPTH == 32:
        QuantumType = c_double if IM_HDRI else c_uint
    elif IM_QUANTUM_DEPTH == 64:
        QuantumType = c_longdouble

    lib.DestroyPixelWand.argtypes = [c_void_p]
    lib.DestroyPixelWand.restype = c_void_p
    lib.IsPixelWand.argtypes = [c_void_p]
    lib.IsPixelWandSimilar.argtypes = [c_void_p, c_void_p, c_double]
    lib.NewPixelWand.argtypes = []
    lib.NewPixelWand.restype = c_void_p
    lib.PixelClearException.argtypes = [c_void_p]
    lib.PixelGetAlpha.argtypes = [c_void_p]
    lib.PixelGetAlpha.restype = c_double
    lib.PixelGetAlphaQuantum.argtypes = [c_void_p]
    lib.PixelGetAlphaQuantum.restype = QuantumType
    lib.PixelGetBlue.argtypes = [c_void_p]
    lib.PixelGetBlue.restype = c_double
    lib.PixelGetBlueQuantum.argtypes = [c_void_p]
    lib.PixelGetBlueQuantum.restype = QuantumType
    lib.PixelGetColorAsNormalizedString.argtypes = [c_void_p]
    lib.PixelGetColorAsNormalizedString.restype = c_magick_char_p
    lib.PixelGetColorAsString.argtypes = [c_void_p]
    lib.PixelGetColorAsString.restype = c_magick_char_p
    lib.PixelGetColorCount.argtypes = [c_void_p]
    lib.PixelGetColorCount.restype = c_size_t
    lib.PixelGetException.argtypes = [c_void_p, POINTER(c_int)]
    lib.PixelGetException.restype = c_magick_char_p
    lib.PixelGetGreen.argtypes = [c_void_p]
    lib.PixelGetGreen.restype = c_double
    lib.PixelGetGreenQuantum.argtypes = [c_void_p]
    lib.PixelGetGreenQuantum.restype = QuantumType
    lib.PixelGetMagickColor.argtypes = [c_void_p, c_void_p]
    if is_im_7:
        lib.PixelGetPixel.argtypes = [c_void_p]
        lib.PixelGetPixel.restype = c_void_p
    lib.PixelGetRed.argtypes = [c_void_p]
    lib.PixelGetRed.restype = c_double
    lib.PixelGetRedQuantum.argtypes = [c_void_p]
    lib.PixelGetRedQuantum.restype = QuantumType
    lib.PixelSetColor.argtypes = [c_void_p, c_char_p]
    if is_im_6:
        lib.PixelSetMagickColor.argtypes = [c_void_p, c_void_p]
        lib.PixelSetPixelColor = None
    if is_im_7:
        lib.PixelSetMagickColor = None
        lib.PixelSetPixelColor.argtypes = [c_void_p, c_void_p]
