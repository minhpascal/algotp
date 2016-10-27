#!/usr/bin/env python3

from collections import namedtuple


class DataModel():
    fields = []
    __fieldItem__ = namedtuple('field', ['name', 'type'])

    def __init__(me, fields=None):
        """ @params {list} fields - list of named tuples
            tuple with keys = name, type
            or list of lists [[name, type], ...]
        """

        if fields is not None:

            for field_def in fields:
                field = field_def
                if(type(field_def) is not namedtuple):
                    field = me.__fieldItem__(
                        name=field_def[0],
                        type=field_def[1])
                me.fields.append(field)

    def setData(me, data):
        # for field in data:
        #     pass
        #     #convert to type defs
        #     ...
        me.data = data

    def getData(me):
        return me.data
