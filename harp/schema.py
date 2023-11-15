from os import PathLike
from typing import TextIO, Union
from harp.model import Model, Registers
from pydantic_yaml import parse_yaml_raw_as
from importlib import resources


def _read_common_registers() -> Registers:
    file = resources.files(__package__) / "common.yml"
    with file.open("rt") as fileIO:
        return parse_yaml_raw_as(Registers, fileIO.read())


def read_schema(
    file: Union[str, PathLike, TextIO], include_common_registers: bool = True
) -> Model:
    if isinstance(file, (str, PathLike)):
        with open(file) as fileIO:
            return read_schema(fileIO)
    else:
        schema = parse_yaml_raw_as(Model, file.read())
        if not "WhoAmI" in schema.registers and include_common_registers:
            common = _read_common_registers()
            schema.registers = dict(common.registers, **schema.registers)
            if schema.bitMasks is not None and common.bitMasks is not None:
                schema.bitMasks = dict(common.bitMasks, **schema.bitMasks)
            if schema.groupMasks is not None and common.groupMasks is not None:
                schema.groupMasks = dict(common.groupMasks, **schema.groupMasks)
        return schema
