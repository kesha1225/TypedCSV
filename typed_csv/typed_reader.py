from csv import *
import typing
from _csv import reader
from pydantic import BaseModel
from typing import Generic, TypeVar


__all__ = [
    "QUOTE_MINIMAL",
    "QUOTE_ALL",
    "QUOTE_NONNUMERIC",
    "QUOTE_NONE",
    "Error",
    "Dialect",
    "excel",
    "excel_tab",
    "field_size_limit",
    "reader",
    "writer",
    "register_dialect",
    "get_dialect",
    "list_dialects",
    "Sniffer",
    "unregister_dialect",
    "DictReader",
    "DictWriter",
    "unix_dialect",
    "TypedReader",
    "BaseModel",
]

T = TypeVar("T")


class TypedReader(Generic[T]):
    def __init__(
        self,
        csvfile: typing.Iterable[str],
        model: typing.Type[T],
        list_delimiter: str = " ",
        fieldnames: typing.Optional[typing.List[str]] = None,
        restkey: typing.Optional[str] = None,
        restval: typing.Optional[str] = None,
        dialect: str = "excel",
        *args,
        **kwargs
    ):
        """
        :param csvfile: - file with csv
        :param model: - pydantic model for csv data
        :param list_delimiter: - delimiter for split list values in csv
        :param fieldnames: - list of keys for the dict
        :param restkey: - key to catch long rows
        :param restval: - default value for short rows
        :param dialect:
        :param args:
        :param kwargs:
        """
        self._fieldnames = fieldnames
        self.model = model
        self.restkey = restkey
        self.restval = restval
        self.reader = reader(csvfile, dialect, *args, **kwargs)
        self.dialect = dialect
        self.line_num = 0

        self.list_delimiter = list_delimiter
        self.validators = {}

        for field, value in self.model.__fields__.items():
            if not isinstance(value.type_, str):
                self.validators[field] = value.type_
            if "List" in str(value.outer_type_):
                self.validators[field] = lambda lst: lst.split(self.list_delimiter)

    def __iter__(self) -> "TypedReader[T]":
        return self

    def set_first_fieldnames(self) -> None:
        if self._fieldnames is None:
            try:
                self._fieldnames = next(self.reader)
            except StopIteration:
                pass
        self.line_num = self.reader.line_num

    @property
    def fieldnames(self) -> typing.List[str]:
        if self._fieldnames is None:
            try:
                self._fieldnames = next(self.reader)
            except StopIteration:
                pass
        self.line_num = self.reader.line_num
        return self._fieldnames

    @fieldnames.setter
    def fieldnames(self, value) -> None:
        self._fieldnames = value

    def __next__(self) -> T:
        if self.line_num == 0:
            self.set_first_fieldnames()
        row = next(self.reader)
        self.line_num = self.reader.line_num

        while not row:
            row = next(self.reader)

        row_dict = dict(zip(self.fieldnames, row))
        lf = len(self.fieldnames)
        lr = len(row)

        if lf < lr:
            row_dict[self.restkey] = row[lf:]
        elif lf > lr:
            for key in self.fieldnames[lr:]:
                row_dict[key] = self.restval
        for field_name, value in row_dict.copy().items():
            if field_name in self.validators:
                row_dict[field_name] = self.validators[field_name](value)
        return self.model(**row_dict)