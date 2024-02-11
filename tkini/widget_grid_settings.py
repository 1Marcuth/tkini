from typing import Optional, Union
from pydantic import validate_call
from tkinter import Tk

from ._types import AnyWidget

class WidgetGridSettings(dict):
    VALIDATE_CONFIG = dict(arbitrary_types_allowed = True)

    @validate_call(config = VALIDATE_CONFIG)
    def __init__(
        self,
        widget: AnyWidget,
        column: int,
        row: int,
        columnspan: Optional[int] = None,
        in_: Optional[Union[AnyWidget, Tk]] = None,
        ipadx: Optional[int] = None,
        ipady: Optional[int] = None,
        padx: Optional[int] = None,
        pady: Optional[int] = None,
        rowspan: Optional[int] = None,
        sticky: Optional[str] = None
    ) -> None:
        super().__init__()
        self["widget"] = widget
        self["column"] = column
        self["row"] = row

        if columnspan is not None:
            self["columnspan"] = columnspan

        if in_ is not None:
            self["in"] = in_

        if ipadx is not None:
            self["ipadx"] = ipadx

        if ipady is not None:
            self["ipady"] = ipady

        if padx is not None:
            self["padx"] = padx

        if pady is not None:
            self["pady"] = pady

        if rowspan is not None:
            self["rowspan"] = rowspan

        if sticky is not None:
            self["sticky"] = sticky