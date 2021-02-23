from sdvs import __version__


def test_version():
    assert len(__version__.split('.')) == 3
