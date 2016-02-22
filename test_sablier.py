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

def test_sub_not_implemented():
    s = sablier.On(2015, 4, 21).At(11).In('Sydney')
    with pytest.raises(TypeError):
        s - 1

def test_sub_sablier():
    a = sablier.On(2015, 5, 23).At(0, 15).In('Sydney')
    b = sablier.On(2015, 5, 22).At(15, 15).In('Paris')
    assert a - b == datetime.timedelta(hours=1)

def test_sub_timedelta():
    a = sablier.On(2015, 5, 23).At(0, 15).In('Sydney')
    d = datetime.timedelta(hours=1)
    assert a - d == sablier.On(2015, 5, 22).At(23, 15).In('Sydney')

def test_add_timedelta():
    a = sablier.On(2015, 5, 22).At(23, 15).In('Sydney')
    d = datetime.timedelta(hours=2)
    assert a + d == sablier.On(2015, 5, 23).At(1, 15).In('Sydney')

def test_fuzzy_matching_difflib_match():
    with pytest.raises(sablier.AmbiguousTimezone):
        sablier.disambiguate('HongKong')

def test_repr_timezone_not_set():
    repr(sablier.On(2015, 10, 15))

def test_on_no_args_today():
    assert sablier.On().date == datetime.date.today()

def test_at_no_args_now():
    assert almost_equal(sablier.At().time, datetime.datetime.now().time())

def test_on_at_no_args():
    s = sablier.On().At()
    now = datetime.datetime.now()
    assert s.date == now.date()
    assert almost_equal(s.time, now.time())

def test_at_on_no_args():
    s = sablier.At().On()
    assert s.date == datetime.date.today()
    assert almost_equal(s.time, datetime.datetime.now().time())

def test_no_match():
    with pytest.raises(sablier.UnknownTimezone):
        sablier.In('Sdney').On().At()

def test_from_datetime():
    now =  datetime.datetime.now()
    s = sablier.Datetime(now)
    assert s.date == now.date()
    assert s.time == now.time()

def almost_equal(left, right):
    """True when (hour, minute, second) equal"""
    return (left.hour, left.minute, left.second) == (right.hour, right.minute, right.second)
