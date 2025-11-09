#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from inspect import Signature, Parameter


def make_sig(names):
    return Signature(
        [Parameter(name, Parameter.POSITIONAL_OR_KEYWORD) for name in names]
    )


class MakeSigMeta(type):
    def __new__(mcls, clsname, bases, clsdict):
        clsdict["__signature__"] = make_sig(clsdict["_fields"])
        return super().__new__(mcls, clsname, bases, clsdict)


class MakeSigStruct(metaclass=MakeSigMeta):
    _fields = []

    def __init__(self, *args, **kwargs):
        bound_args = self.__signature__.bind(*args, **kwargs)
        for name, value in bound_args.arguments.items():
            setattr(self, name, value)


class Stock(MakeSigStruct):
    _fields = ["name", "shares", "price"]


class Point(MakeSigStruct):
    _fields = ["x", "y"]


if __name__ == "__main__":
    s1 = Stock("ACME", 93, 490.1)
    print(s1.name, s1.shares, s1.price)
    s2 = Stock("ACME", 93)
    # s3 = Stock(name="ACME", shares=93, name="ACME", price=490.1)
