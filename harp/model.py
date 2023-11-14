# generated by datamodel-codegen:
#   filename:  device.json
#   timestamp: 2023-10-30T11:46:57+00:00

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional, Union
from typing_extensions import Annotated

from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    RootModel,
    conint,
    field_serializer,
)


class PayloadType(str, Enum):
    U8 = "uint8"
    S8 = "int8"
    U16 = "uint16"
    S16 = "int16"
    U32 = "uint32"
    S32 = "int32"
    U64 = "uint64"
    S64 = "int64"
    Float = "float32"


class Access(Enum):
    Read = "Read"
    Write = "Write"
    Event = "Event"


class MaskValueItem(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    value: int = Field(..., description="Specifies the numerical mask value.")
    description: Optional[str] = Field(
        None, description="Specifies a summary description of the mask value function."
    )

    def __int__(self):
        return self.value


class MaskValue(RootModel[Union[int, MaskValueItem]]):
    root: Union[int, MaskValueItem]


class BitMask(BaseModel):
    description: Optional[str] = Field(
        None, description="Specifies a summary description of the bit mask function."
    )
    bits: Dict[str, MaskValue]


class GroupMask(BaseModel):
    description: Optional[str] = Field(
        None, description="Specifies a summary description of the group mask function."
    )
    values: Dict[str, MaskValue]


class MaskType(RootModel[str]):
    root: str = Field(
        ...,
        description="Specifies the name of the bit mask or group mask used to represent the payload value.",
    )


class InterfaceType(RootModel[str]):
    root: str = Field(
        ...,
        description="Specifies the name of the type used to represent the payload value in the high-level interface.",
    )


class Converter(Enum):
    None_ = "None"
    Payload = "Payload"
    RawPayload = "RawPayload"


class MinValue(RootModel[float]):
    root: float = Field(
        ...,
        description="Specifies the minimum allowable value for the payload or payload member.",
    )


class MaxValue(RootModel[float]):
    root: float = Field(
        ...,
        description="Specifies the maximum allowable value for the payload or payload member.",
    )


class DefaultValue(RootModel[float]):
    root: float = Field(
        ...,
        description="Specifies the default value for the payload or payload member.",
    )


class PayloadMember(BaseModel):
    mask: Optional[int] = Field(
        None,
        description="Specifies the mask used to read and write this payload member.",
    )
    offset: Optional[int] = Field(
        None,
        description="Specifies the payload array offset where this payload member is stored.",
    )
    description: Optional[str] = Field(
        None, description="Specifies a summary description of the payload member."
    )
    minValue: Optional[MinValue] = None
    maxValue: Optional[MaxValue] = None
    defaultValue: Optional[DefaultValue] = None
    maskType: Optional[MaskType] = None
    interfaceType: Optional[InterfaceType] = None
    converter: Optional[Converter] = None


class Visibility(Enum):
    public = "public"
    private = "private"


class Register(BaseModel):
    address: conint(le=255) = Field(
        ..., description="Specifies the unique 8-bit address of the register."
    )
    type: Annotated[PayloadType, BeforeValidator(lambda v: PayloadType[v])]
    length: Optional[conint(ge=1)] = Field(
        default=1, description="Specifies the length of the register payload."
    )
    access: Union[Access, List[Access]] = Field(
        ..., description="Specifies the expected use of the register."
    )
    description: Optional[str] = Field(
        None, description="Specifies a summary description of the register function."
    )
    minValue: Optional[MinValue] = None
    maxValue: Optional[MaxValue] = None
    defaultValue: Optional[DefaultValue] = None
    maskType: Optional[MaskType] = None
    visibility: Optional[Visibility] = Field(
        None,
        description="Specifies whether the register function is exposed in the high-level interface.",
    )
    volatile: Optional[bool] = Field(
        None,
        description="Specifies whether register values can be saved in non-volatile memory.",
    )
    payloadSpec: Optional[Dict[str, PayloadMember]] = None
    interfaceType: Optional[InterfaceType] = None
    converter: Optional[Converter] = None

    @field_serializer("type")
    def _serialize_type(self, type: PayloadType):
        return type.name


class Registers(BaseModel):
    registers: Dict[str, Register] = Field(
        ...,
        description="Specifies the collection of registers implementing the device function.",
    )
    bitMasks: Optional[Dict[str, BitMask]] = Field(
        None,
        description="Specifies the collection of masks available to be used with the different registers.",
    )
    groupMasks: Optional[Dict[str, GroupMask]] = Field(
        None,
        description="Specifies the collection of group masks available to be used with the different registers.",
    )


class Model(Registers):
    device: str = Field(..., description="Specifies the name of the device.")
    whoAmI: int = Field(
        ..., description="Specifies the unique identifier for this device type."
    )
    firmwareVersion: str = Field(
        ..., description="Specifies the semantic version of the device firmware."
    )
    hardwareTargets: str = Field(
        ..., description="Specifies the semantic version of the device hardware."
    )
