from typing import Annotated

from fastapi import Path

EntityID = Annotated[int, Path(..., gt=0)]
