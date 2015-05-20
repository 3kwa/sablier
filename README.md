sablier
=======

It is hard to find a good name for a module that's meant to relieve the pain
of working with date, time and timezones.

`sablier` means hourglass in French and really is just a DSL like API to turn
timezone into something kind of fun.


Constructors
============

How do you like to write about time?

* `In` Paris `On` the first of April 2015 `At` 12:30
* or `At` 12:30 `On` the first of April 2015 `In` Paris
* or ...

You get the gist! You pick e.g.

    >>> from sablier import In
    >>> In('Japan').On(2015, 5, 20).At(11)
    Sablier(datetime.date(2015, 5, 20), datetime.time(11, 0), 'Japan')

Every time you chain a new `In`, the *underlying* datetime is `astimezone`d
(well technically the first `In` is `localize`d but ... maked ones head hurt).
A convenient way to get what ones want is to call one of the
3 converters.

Converters
==========

`date_in`
---------

    >>> from sablier import On
    >>> On(2015, 5, 20).At(23).date_in('Sydney')
    datetime.date(2015, 5, 21)

If no `In` is chained it is UTC. `sablier` does not do *naive*!

`time_in`
---------

    >>> In('Singapore').On(2015, 5, 20).At(15, 30, 5).time_in('US/Pacific')
    datetime.time(0, 30, 5)


`datetime_in`
-------------

    >>> On(2015, 5, 20).At(23).In('Moscow').datetime_in('Paris')
    datetime.datetime(2015, 5, 21, 1, 0, tzinfo=<DstTzInfo 'Europe/Paris' CEST+2:00:00 DST>)

Yep you can still get into the tzinfo dark art if you want.

Epoch
=====

An extra constructor for the touch more obscure yet common use case of having
an epoch timestamp to start with.

    >>> from sablier import Epoch
    >>> Epoch(1432123319)
    Sablier(datetime.date(2015, 5, 20), datetime.time(12, 1, 59), 'UTC')
