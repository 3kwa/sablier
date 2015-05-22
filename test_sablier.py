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

def test_at_args():
    s = sablier.At(13, 30).On(2015, 5, 20)
    assert s.time == datetime.time(13, 30)

def test_at_time():
    s = sablier.At(datetime.time(13)).On(2015, 5, 20)
    assert s.time == datetime.time(13)

def test_on_date():
    s = sablier.At(13, 30).On(datetime.date(2015, 5, 20))
    assert s.date == datetime.date(2015, 5, 20)

def test_in_on_at():
    s = sablier.In('Sydney').On(2015, 5, 21).At(11)
    assert s == sablier.Sablier(datetime.date(2015, 5, 21),
                                datetime.time(11),
                                'Australia/Sydney')

def test_on_at_in():
    s = sablier.On(2015, 5, 21).At(11).In('London')
    assert s == sablier.Sablier(datetime.date(2015, 5, 21),
                                datetime.time(11),
                                'Europe/London')
