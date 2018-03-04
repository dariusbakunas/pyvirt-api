# coding=utf-8
from types import MethodType


def dict_to_libvirt_obj(d):
    """
    All libvirt object props are methods, this helper adds ability to access all
    dict props as methods (used in tests)
    :param d: dictionary that we want to convert
    :return: object where all properties can be accessed as methods
    """
    o = type('', (), {"data": d})()
    for key in d.keys():
        setattr(o, key, MethodType(lambda self, param=key: self.data[param], o))
    return o