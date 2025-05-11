from typing import Sequence

from pydantic import BaseModel


class SequenceResponse[T](BaseModel):
    items: Sequence[T]
    total_count: int
