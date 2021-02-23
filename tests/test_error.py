from pytest import raises

from sdvs.error import BaseError


def test_baseerror():
    with raises(BaseError):
        raise BaseError()
