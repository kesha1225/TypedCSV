from _csv import writer
from pydantic import BaseModel

import typing

from ._types import _DialectLike, _Writer


class TypedWriter:
    def __init__(
        self,
        csvfile: _Writer,
        model: typing.Type[BaseModel],
        restval: typing.Optional[typing.Any] = "",
        extrasaction: str = "raise",
        dialect: _DialectLike = "excel",
        list_delimiter: typing.Optional[str] = ",",
        *args: typing.Any,
        **kwargs: typing.Any,
    ):
        """
        :param csvfile: - file with csv
        :param model: - pydantic model for csv data
        :param restval: - for writing short dicts
        :param extrasaction: - reaction on wrong fields
        :param dialect: - csv dialect
        :param list_delimiter: - delimiter for split list values in csv
        :param args:
        :param kwargs:
        """
        self.model = model
        self.list_delimiter = list_delimiter

        self.fieldnames: typing.List[str] = list(self.model.__fields__.keys())
        self.restval = restval

        if extrasaction.lower() not in ("raise", "ignore"):
            raise ValueError(
                f"extrasaction ({extrasaction}) must be 'raise' or 'ignore'"
            )
        self.extrasaction = extrasaction
        self.writer = writer(csvfile, dialect, *args, **kwargs)

    def writeheader(self):
        header = dict(zip(self.fieldnames, self.fieldnames))
        self.writerow(header)

    def _model_to_list(self, model: BaseModel) -> typing.List[str]:
        model_dict = model.dict()

        if self.extrasaction == "raise":
            wrong_fields = model_dict.keys() - self.fieldnames
            if wrong_fields:
                raise ValueError(
                    f"model contains fields not in fieldnames: {', '.join([repr(x) for x in wrong_fields])}"
                )

        raw_values = [model_dict.get(key, self.restval) for key in self.fieldnames]
        values = []
        for raw_value in raw_values:
            if isinstance(raw_value, list):
                values.append(self.list_delimiter.join(raw_value))
                continue
            values.append(raw_value)
        return values

    def writerow(self, model: typing.Union[dict, BaseModel]):
        if isinstance(model, dict):
            return self.writer.writerow(model)
        return self.writer.writerow(self._model_to_list(model))

    def writerows(self, models: typing.List[BaseModel]):
        return self.writer.writerows(map(self._model_to_list, models))
