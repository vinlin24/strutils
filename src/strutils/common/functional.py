import dataclasses
from typing import TypeVar

from typing_extensions import dataclass_transform

T = TypeVar("T")


# See: https://stackoverflow.com/a/73422882/14226122
@dataclass_transform(frozen_default=True, kw_only_default=True)
def readonly_struct(cls: type[T]) -> type[T]:
    return dataclasses.dataclass(frozen=True, kw_only=True)(cls)
