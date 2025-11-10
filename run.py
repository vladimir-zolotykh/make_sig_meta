#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Any
from inspect import Signature, Parameter
import unittest


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


def as_tuple(s: MakeSigStruct) -> tuple[Any, ...]:
    return tuple(s.__dict__.values())


class Stock(MakeSigStruct):
    _fields = ["name", "shares", "price"]


class Point(MakeSigStruct):
    _fields = ["x", "y"]


class TestMakeSig(unittest.TestCase):
    def test_10(self):
        s1 = Stock("ACME", 93, 490.1)
        self.assertEqual(as_tuple(s1), ("ACME", 93, 490.1))

    def test_20(self):
        with self.assertRaises(TypeError) as cm:
            Stock("ACME", 93)
        self.assertEqual(str(cm.exception), "missing a required argument: 'price'")

    def test_30(self):
        with self.assertRaises(TypeError) as cm:
            Stock("ACME", 100, 490.1, shares=50)
        self.assertEqual(str(cm.exception), "multiple values for argument 'shares'")


if __name__ == "__main__":
    unittest.main()
