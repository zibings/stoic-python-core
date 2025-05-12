# NodeBase.py
from abc import ABC, abstractmethod
from typing import List, Any, Optional, Type

# Import the DispatchBase class (will be defined in another file)
from .dispatch_base import DispatchBase


def is_dispatch_of_type(dispatch: DispatchBase, *classes: Type) -> bool:
    """
    Return whether dispatch is an instance of any provided classes.

    Args:
        dispatch: Dispatch object to check
        *classes: Classes to check against

    Returns:
        bool: True if dispatch is an instance of any provided class, False otherwise
    """
    for cls in classes:
        if isinstance(dispatch, cls):
            return True

    return False


class NodeBase(ABC):
    """
    Abstract class to provide contract for all nodes used with the chain system.
    """

    def __init__(self):
        """Initialize a new NodeBase instance."""
        self._key: Optional[str] = None
        self._version: Optional[str] = None

    def __str__(self) -> str:
        """Serialize object as a string."""
        return f"{self.__class__.__name__}{{ \"key\": \"{self._key}\", \"version\": \"{self._version}\" }}"

    def get_key(self) -> str:
        """Return the node key value."""
        return self._key

    def get_version(self) -> str:
        """Return the node version value."""
        return self._version

    def is_valid(self) -> bool:
        """
        Return whether the node is considered valid. This means that there are
        non-empty values in both the 'key' and 'version' fields of the node by default.

        Returns:
            bool: True if node is valid, False otherwise
        """
        return bool(self._key) and bool(self._version)

    @abstractmethod
    def process(self, sender: Any, dispatch: DispatchBase) -> None:
        """
        Abstract method that handles processing of a provided dispatch.

        Args:
            sender: Sender data, optional and thus can be None
            dispatch: Dispatch object to process
        """
        pass

    def set_key(self, key: str) -> 'NodeBase':
        """
        Set the node key value.

        Args:
            key: Value to use for node key

        Returns:
            NodeBase: Self for method chaining
        """
        self._key = key
        return self

    def set_version(self, version: str) -> 'NodeBase':
        """
        Set the node version value.

        Args:
            version: Value to use for node version

        Returns:
            NodeBase: Self for method chaining
        """
        self._version = version
        return self