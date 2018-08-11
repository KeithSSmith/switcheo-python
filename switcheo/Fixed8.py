# -*- coding:utf-8 -*-
"""
Description:
    Fixed8

Usage:
    from neocore.Fixed8 import Fixed8
"""

from neocore.Fixed8 import Fixed8
from switcheo.utils import reverse_hex


def num2fixed8(number, size=8):
    if size % 1 != 0:
        raise ValueError('Fixed8 size {} is not a whole number.'.format(size))
    return SwitcheoFixed8(float("{:.8f}".format(number))).toReverseHex()[:size*2]


class SwitcheoFixed8(Fixed8):

    def toHex(self):
        hexstring = hex(round(self.value * self.D))[2:]
        return "{:0>16s}".format(hexstring)

    def toReverseHex(self):
        return reverse_hex(self.toHex())
