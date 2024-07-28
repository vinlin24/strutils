import dataclasses
from typing import TypeVar

import typing_extensions

T = TypeVar("T")


# See: https://stackoverflow.com/a/73422882/14226122
@typing_extensions.dataclass_transform(eq_default=True, kw_only_default=True)
def program_options_struct(cls: type[T]) -> type[T]:
    return dataclasses.dataclass(frozen=True, kw_only=True)(cls)
