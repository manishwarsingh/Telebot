"""
csv342 is a Python module similar to the the csv module in the standard
library. Under Python 3, it just calls the standard csv module. Under
Python 2, it provides a Python 3 like interface to reading and writing CSV
files, in particular concerning non ASCII characters.

It is distributed under the BSD license with the source code available from
https://github.com/roskakori/csv342.
"""
# Copyright (c) 2016-2020, Thomas Aglassinger
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of csv342 nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
from __future__ import unicode_literals

from csv import *
import sys

__version__ = '1.0.1'

IS_PYTHON2 = sys.version_info[0] == 2


if IS_PYTHON2:
    import csv
    import cStringIO
    import io
    import StringIO

    _binary_type = str
    _text_type = unicode
    _type_of_StringI = type(cStringIO.StringIO(''))
    _type_of_StringO = type(cStringIO.StringIO())

    def _key_to_str_value_map(key_to_value_map):
        """
        Similar to ``key_to_value_map`` but with values of type `unicode`
        converted to `str` because in Python 2 `csv.reader` can only process
        byte strings for formatting parameters, e.g. delimiter=b';' instead of
        delimiter=u';'. This quickly becomes an annoyance to the caller, in
        particular with `from __future__ import unicode_literals` enabled.
        """
        return dict((key, value if not isinstance(value, _text_type) else _binary_type(value))
                    for key, value in key_to_value_map.items())

    class _UnicodeCsvWriter(object):
        r"""
        A CSV writer for Python 2 which will write rows to `target_stream`
        which must be able to write unicode strings.

        To obtain a target stream for a file use for example (note the
        ``newline=''``):

        >>> import io
        >>> import os
        >>> import tempfile
        >>> target_path = os.path.join(tempfile.tempdir, 'test_csv342.UnicodeCsvWriter.csv')
        >>> target_stream = io.open(target_path, 'w', newline='', encoding='utf-8')

        This is based on ``UnicodeWriter`` from <https://docs.python.org/2/library/csv.html> but expects the
        target to accept unicode strings.
        """

        def __init__(self, target_stream, dialect=csv.excel, **keywords):
            if isinstance(target_stream, (_type_of_StringO, StringIO.StringIO)):
                raise Error(
                    'use io.StringIO instead of %r for target_stream' %
                    type(target_stream))
            self._target_stream = target_stream
            self._queue = io.BytesIO()
            str_keywords = _key_to_str_value_map(keywords)
            self._csv_writer = csv.writer(self._queue, dialect=dialect, **str_keywords)

        def writerow(self, row):
            assert row is not None

            row_as_list = list(row)
            # Convert ``row`` to a list of unicode strings.
            row_to_write = []
            for item in row_as_list:
                if item is None:
                    item = ''
                elif not isinstance(item, _text_type):
                    item = _text_type(item)
                row_to_write.append(item.encode('utf-8'))
            try:
                self._csv_writer.writerow(row_to_write)
            except TypeError as error:
                raise TypeError('%s: %s' % (error, row_as_list))
            data = self._queue.getvalue()
            data = data.decode('utf-8')
            self._target_stream.write(data)
            # Clear the BytesIO before writing the next row.
            self._queue.seek(0)
            self._queue.truncate(0)

        def writerows(self, rows):
            for row in rows:
                self.writerow(row)

    class _Utf8Recoder(object):
        """
        Iterator that reads a text stream and reencodes the input to UTF-8.
        """
        def __init__(self, text_stream):
            if isinstance(text_stream, StringIO.StringIO):
                raise Error('StringIO.StringIO for CSV must be changed to io.StringIO')
            self._text_stream = iter(text_stream)

        def __iter__(self):
            return self

        def __next__(self):
            return self._text_stream.next().encode('utf-8')

        def next(self):
            return self.__next__()

    class _UnicodeCsvReader(object):
        """
        A CSV reader which will iterate over lines in the CSV file 'csv_file',
        which is encoded in the given encoding.
        """

        def __init__(self, csv_file, dialect=csv.excel, **keywords):
            csv_file = _Utf8Recoder(csv_file)
            str_keywords = _key_to_str_value_map(keywords)
            self.reader = csv.reader(csv_file, dialect=dialect, **str_keywords)
            self.line_num = -1

        def __next__(self):
            self.line_num += 1
            row = self.reader.next()
            result = [item.decode('utf-8') for item in row]
            return result

        def next(self):
            return self.__next__()

        def __iter__(self):
            return self


    def reader(source_text_stream, dialect=csv.excel, **keywords):
        """
        Same as Python 3's `csv.reader` but works with Python 2.
        """
        assert source_text_stream is not None

        return _UnicodeCsvReader(source_text_stream, dialect=dialect, **keywords)


    def writer(target_text_stream, dialect=csv.excel, **keywords):
        """
        Same as Python 3's `csv.writer` but works with Python 2.
        """
        assert target_text_stream is not None

        return _UnicodeCsvWriter(target_text_stream, dialect=dialect, **keywords)


    class DictReader:
        def __init__(self, input_stream, fieldnames=None, restkey=None, restval=None,
                     dialect="excel", *args, **kwds):
            self._fieldnames = fieldnames
            self.restkey = restkey
            self.restval = restval
            self.reader = reader(input_stream, dialect, *args, **kwds)
            self.dialect = dialect

        def __iter__(self):
            return self

        def _set_fieldnames_from_first_row(self):
            assert self._fieldnames is None
            self._fieldnames = next(self.reader)

        @property
        def fieldnames(self):
            if self._fieldnames is None:
                try:
                    self._set_fieldnames_from_first_row()
                except StopIteration:
                    pass
            return self._fieldnames

        @fieldnames.setter
        def fieldnames(self, value):
            self._fieldnames = value

        @property
        def line_num(self):
            return self.reader.line_num


        def __next__(self):
            if self.fieldnames is None:
                self._set_fieldnames_from_first_row()
            fieldvalues = next(self.reader)

            # Skip empty lines to avoid lists of None.
            while len(fieldvalues) == 0:
                fieldvalues = next(self.reader)

            result = dict(zip(self.fieldnames, fieldvalues))
            fieldnames_count = len(self.fieldnames)
            fieldvalue_count = len(fieldvalues)
            if fieldnames_count < fieldvalue_count:
                result[self.restkey] = fieldvalues[fieldnames_count:]
            elif fieldnames_count > fieldvalue_count:
                for key in self.fieldnames[fieldvalue_count:]:
                    result[key] = self.restval
            return result

        def next(self):
            return self.__next__()


    class DictWriter:
        def __init__(self, stream, fieldnames, restval="", extrasaction='raise',
                     dialect='excel', *args, **kwds):
            self.fieldnames = fieldnames
            self.restval = restval
            if extrasaction.lower() not in ('ignore', 'raise'):
                raise ValueError(
                    "extrasaction (%s) must be 'raise' or 'ignore'" %
                    extrasaction)
            self.extrasaction = extrasaction
            self.writer = writer(stream, dialect, *args, **kwds)

        def writeheader(self):
            header = dict(zip(self.fieldnames, self.fieldnames))
            self.writerow(header)

        def _dict_to_list(self, row_dict):
            if self.extrasaction == 'raise':
                unknown_fields = [
                    key for key in row_dict if key not in self.fieldnames
                    ]
                if unknown_fields:
                    raise ValueError(
                        "dict contains fields not in fieldnames: " +
                        ", ".join([repr(x) for x in unknown_fields]))
            return [row_dict.get(key, self.restval) for key in self.fieldnames]

        def writerow(self, row_dict):
            return self.writer.writerow(self._dict_to_list(row_dict))

        def writerows(self, row_dicts):
            rows = []
            for row_dict in row_dicts:
                rows.append(self._dict_to_list(row_dict))
            return self.writer.writerows(rows)


if __name__ == '__main__':
    if IS_PYTHON2:  # Doctests only work with Python 2 due u'...' prefix mess.
        import doctest
        print('csv342 {0}: running doctest'.format(__version__))
        doctest.testmod()
