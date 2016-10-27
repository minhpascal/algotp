#!/usr/bin/env python3

import abc
from lib.abstract_base import AbstractBase

class AbstractReader(AbstractBase):
    __metaclass__ = abc.ABCMeta

    def __init__(me):
        pass

    @abc.abstractmethod
    def read(me, *args, **kwargs):
        """
            returns False if no data exists at specified position
        """
        pass


class AbstractWriter(AbstractBase):
    __metaclass__ = abc.ABCMeta

    def __init__(me):
        pass

    @abc.abstractmethod
    def write(me, *args, **kwargs):
        pass



class AbstractProvider(AbstractBase):
    __metaclass__ = abc.ABCMeta
    reader = None
    writer = None

    def __init__(me, reader, writer):
        me.reader = reader
        me.writer = writer

    @abc.abstractmethod
    def fetch(me):
        pass

    def write(me, *args, **kwargs):
        me.writer.write(*args, **kwargs)

    def read(me, *args, **kwargs):
        """
            returns False if no data exists at specified position
        """
        yield me.reader.read(*args, **kwargs)

    def get_data(me, *args, **kwargs):

        yield me.__read_or_fetch__(*args, **kwargs)

    def __read_or_fetch__(me, *args, **kwargs):
        for data in me.read(*args, **kwargs):

            if type(data) is bool and data is False:
                # data or file doesnt exist
                print('@read_or_fetch: fetching ...')
                yield me.fetch_data(*args, **kwargs)

            else:
                print('@read_or_fetch: found data', data)
                yield data
