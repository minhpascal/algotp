#!/usr/bin/env python3

from collections import namedtuple
import pandas as pd
from contextlib import contextmanager
from .abstract_io import AbstractReader, AbstractWriter
from lib.util.path import build_file_path, create_dir_if_not_exist


class HDFReader(AbstractReader):
    def __init__(me):
        pass

    def read(me, table_key=None, **opt):
        """
            yields False if no data exists at specified position
        """
        print('date between:', opt.get('dt_first'), opt.get('dt_last'))

        # dt_first/last should be datetime objects

        dt_first = opt.get('dt_first')
        dt_last = opt.get('dt_last')

        where = 'index >= dt_first & index <= dt_last'

        for file in build_file_path(ext='h5',
                                    symbol=opt.get('symbol'),
                                    provider=opt.get('provider'),
                                    data_type=opt.get('data_type'),
                                    candle_format=opt.get('candle_format'),
                                    granularity=opt.get('granularity'),
                                    dt_first=opt.get('dt_first'),
                                    dt_last=opt.get('dt_last')):

            yield me.get_hdf_table(file_path=file.path,
                                   table_key=table_key,
                                   where=where,
                                   iterable=True, **opt)

    @contextmanager
    def open_hdf(me, file_path):
        try:
            store = False
            store = pd.HDFStore(file_path, mode='r+')
            store.open()
            yield store
        except Exception as e:
            me.log('@open_hdf exception, store type', type(store), e)
            yield False
        finally:
            if store is not False:
                store.close()
                me.log('\n @filepath:%s \nclosing store...' % file_path)

    def get_hdf_table(me, file_path=None, where=None, table_key=None,
                      iterable=True, **options):
        """ attempts to open hdf5 file if it fails returns False
            otherwise returns an iterable table data set
            """
        # table_key = options.get('table_key')
        chunksize = options.get('chunksize')
        dt_first = options.get('dt_first')
        dt_last = options.get('dt_last')
        # me.log('getting data')

        with me.open_hdf(file_path) as store:
            # print('\nstore at get table\n', store)
            if type(store) is bool and store is False:
                me.log('store is false so file doesnt exist\n')

                # file doesn't exist
                return False
            else:
                try:
                    t = store.select(table_key, #where=where,
                                        iterable=iterable,
                                        chunksize=chunksize)
                    me.log('@get_hdf : yielding ... \n%s'%t.head())

                    # yield from store.select(table_key, where=where,
                    return t
                except Exception as e:
                    # !table doesnt exist , attempt to download data

                    me.log('@exception : could not get table data from ' +
                           table_key + ' ...\n', e, '\n')
                    return False

                    # pd.read_hdf(file,
                    # where='index >= dt_first & index <= dt_last',
                    # iterator=False, chunksize = None )



class HDFWriter(AbstractWriter):
    def __init__(me):
        pass

    def write(me, dataframe, table_key=None, **options):
        """ saves dataframe to hdf5 file by appending it
            if file doesnt exist it is created
        """

        # abort if file/data doesnt exist
        is_df = type(dataframe) is pd.DataFrame
        is_df_empty = dataframe.empty is False
        is_df_ts = type(dataframe.index) is pd.DatetimeIndex

        assert is_df and is_df_empty, 'data is empty or not a dataframe'
        assert is_df_ts, 'expected timeseries data'
        # get the first and last indexs from dataframe
        # df_first_index = dataframe.first_valid_index()
        # df_last_index = dataframe.last_valid_index()

        # table_key = options.get('table_key')
        for file in build_file_path(**options):
            # this data will be save in file_path
            cond1 = (dataframe.index.weekofyear == file.week)
            cond2 = (dataframe.index.year == file.year)

            frame = dataframe[cond1 & cond2]

            create_dir_if_not_exist(file.path)

            # open file in append mode
            # creates file if it doesnt exist already
            store = pd.HDFStore(file.path)

            try:
                # select existing
                ts = store.select(table_key)

                # check the last index in the file and see if data is already
                # their
                db_last_index = ts.index.max()

                # do somethin with this: later
                # check for duplicates/overlaps,
                # and decide what to do with data,
                # also drop nans
                # overlapping = ...
                # ts[(ts.index>=df_first_index) & (ts.index<=df_last_index)]

                print('\n@save: sample dataframe: %s \n' % dataframe.head())

                # !use df.append to prevent duplicate index
                # although this can be memory intensive/killer for sub minute
                # freqs
                ts.append(dataframe, verify_integrity=True)

                # rewrite data
                store.append(table_key, ts,
                             append=False,
                             format='table',
                             chunksize=5000)

                m = (ts.memory_usage().sum() + dataframe.memory_usage().sum())
                print('\n@save memory used: %s \n' % m)



            except KeyError:
                print('\n@save : key error occured')

                # !create new table
                # dummy table to enable us to use the next command *faster?
                store.put(table_key, value=pd.DataFrame(
                    [1, 1, 1], columns=['c1']), format='table')

                store.get_storer(table_key).write(dataframe)
            except ValueError:  # not saving overlaping indexs
                pass
            except Exception as e:
                print(e)
                raise e

            finally:
                #
                store.close()

            # todo: not priority
            # df.difference(ts) # should return none if there no overlap
            # if thier is some data overlap check that the data
            # is the same accross the previous 100 entries
            # if the data is different
            # extend to 1000 on both sides and
            # if data doesnt match
            # save in a diffenent table with postfix_vernum
            # ts
            # df/idx.memory_usage() get usage

