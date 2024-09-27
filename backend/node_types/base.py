from abc import ABC, abstractmethod
from pyclbr import Class
from pydantic import BaseModel
from typing import ClassVar, Generic, Type, TypeVar, get_args, get_origin

from pyparsing import C
from regex import B

ConfigType = TypeVar("ConfigType", bound=BaseModel)
InputType = TypeVar("InputType", bound=BaseModel)
OutputType = TypeVar("OutputType", bound=BaseModel)


class BaseNodeType(Generic[ConfigType, InputType, OutputType], ABC):
    """
    Base class for all node types.
    """

    name: str

    ConfigType: ClassVar[Type[BaseModel]]
    InputType: ClassVar[Type[BaseModel]]
    OutputType: ClassVar[Type[BaseModel]]

    @abstractmethod
    def __init__(self, config: BaseModel) -> None:
        pass

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        if not hasattr(cls, "name"):
            raise NotImplementedError("Node type must define a 'name' property")
        # Iterate over the base classes
        for base in cls.__bases__:
            origin = get_origin(base)
            if origin is BaseNodeType:
                type_args = get_args(base)
                if len(type_args) == 3:
                    cls.InputType, cls.OutputType, cls.ConfigType = type_args
                else:
                    raise TypeError(f"Expected 3 type arguments, got {len(type_args)}")
                break
        else:
            raise TypeError(
                "Generic type parameters not specified for BaseNodeType subclass."
            )

    @abstractmethod
    async def __call__(self, input_data: BaseModel) -> BaseModel:
        """
        Execute the node with the given input data.

        Args:
            input_data (BaseModel): Pydantic model containing input data.

        Returns:
            BaseModel: Pydantic model containing output data.
        """
        pass