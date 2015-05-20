import datetime

import pytest

import sablier


def test_epoch():
    e = sablier.Epoch(1432083030)
    assert e.date == datetime.date(2015, 5, 20)
    assert e.time == datetime.time(0, 50, 30)
    assert e.timezone.zone == 'UTC'

def test_disambiguate_ambiguous():
    with pytest.raises(sablier.AmbiguousTimezone):
        sablier.disambiguate('Europe')

def test_disambiguate_good():
    assert sablier.disambiguate('Paris') == 'Europe/Paris'

