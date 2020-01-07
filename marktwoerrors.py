from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class MarkTwoError(Exception):
    parent: type = field(
            default=None,
            compare=True,
            repr=True,
            init=True
            )
    default_message: str = field(
            default=None,
            compare=True,
            repr=False,
            init=False
            )
    specific_message: str = field(
            default=None,
            compare=True,
            repr=False,
            init=True
            )
    def __post_init__(self) -> None:
        print(self.default_message)
        print(self.specific_message)

@dataclass
class MarkTwoOptionError(MarkTwoError):
    """
    Raised when an illegal option is
    passed into optionparser.parseOpts().
    """
    default_message = "Error getting/setting options."

@dataclass
class MarkTwoParseError(MarkTwoError):
    """
    Raised when an irreconcilable
    situation is met while parsing.
    """
    default_message = "Error parsing input text."
