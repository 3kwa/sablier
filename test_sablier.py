import datetime

from sablier import Epoch


def test_epoch():
    e = Epoch(1432083030)
    assert e.date == datetime.date(2015, 5, 20)
    assert e.time == datetime.time(0, 50, 30)
    assert e.timezone.zone == 'UTC'
