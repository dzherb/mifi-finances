import abc
from collections.abc import Sequence
from datetime import timedelta
from typing import Any, cast, ClassVar, Literal, Protocol

from asyncpg import Connection
from dateutil.relativedelta import relativedelta
from sqlalchemy import AdaptedConnection, event
from sqlalchemy.ext.asyncio import AsyncEngine


class _TypeCodec(Protocol):
    name: ClassVar[str]
    format: ClassVar[Literal['text', 'binary', 'tuple']]

    def encode(self, value: Any) -> Any: ...

    def decode(self, value: Any) -> Any: ...


class StrTypeCodec[T](_TypeCodec):
    name: ClassVar[str]
    format = 'text'

    @abc.abstractmethod
    def encode(self, value: Any) -> str: ...

    @abc.abstractmethod
    def decode(self, value: str) -> T: ...


class BinaryTypeCodec[T](_TypeCodec):
    format = 'binary'

    @abc.abstractmethod
    def encode(self, value: Any) -> bytes: ...

    @abc.abstractmethod
    def decode(self, value: bytes) -> T: ...


class TupleTypeCodec[T](_TypeCodec):
    format = 'tuple'

    @abc.abstractmethod
    def encode(self, value: Any) -> tuple[Any, ...]: ...

    @abc.abstractmethod
    def decode(self, value: tuple[Any, ...]) -> T: ...


class Interval(TupleTypeCodec[relativedelta]):
    name = 'interval'

    def encode(self, value: Any) -> tuple[int, int, int]:
        if isinstance(value, timedelta):
            value = relativedelta(
                seconds=int(value.total_seconds()),
                microseconds=value.microseconds,
            )

        if isinstance(value, relativedelta):
            delta = value.normalized()

            return (
                delta.years * 12 + delta.months,
                delta.days,
                (delta.hours * 3600 + delta.minutes * 60 + delta.seconds)
                * 1000000
                + delta.microseconds,
            )

        raise TypeError(f'Type {type(value)} cannot be encoded as interval')

    def decode(self, value: tuple[Any, ...]) -> relativedelta:
        value = cast(tuple[int, int, int], value)
        return relativedelta(
            months=value[0],
            days=value[1],
            microseconds=value[2],
        )


class TypesRegister:
    def __init__(self, types: Sequence[_TypeCodec]) -> None:
        self.types = types

    def register_for_engine(self, engine: AsyncEngine) -> None:
        on_connect = event.listens_for(engine.sync_engine, 'connect')
        on_connect(self._register_for_adapter)

    def _register_for_adapter(
        self,
        adapter: AdaptedConnection,
        *args: Any,
    ) -> None:
        adapter.run_async(self._register_for_connection)

    async def _register_for_connection(
        self,
        connection: Connection,  # type:ignore[type-arg]
    ) -> None:
        for type_ in self.types:
            await connection.set_type_codec(
                typename=type_.name,
                format=type_.format,
                encoder=type_.encode,
                decoder=type_.decode,
                schema='pg_catalog',
            )


def register(engine: AsyncEngine, types: Sequence[_TypeCodec]) -> None:
    TypesRegister(types).register_for_engine(engine)
