from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import List, Any, Optional


class DispatchBase(ABC):
    """
    Abstract class to provide contract for all dispatches used with the chain system.
    """

    def __init__(self):
        """Initialize a new DispatchBase instance."""
        self._is_consumable: bool = False
        self._is_stateful: bool = False
        self._is_consumed: bool = False
        self._results: List[Any] = []
        self._is_valid: bool = False
        self._called_date_time: Optional[datetime] = None

    def __str__(self) -> str:
        """Serialize the DispatchBase class to a string."""
        called_date_time = self._called_date_time.strftime("%Y-%m-%d %H:%M:%S") if self._called_date_time else 'N/A'

        return (f"{self.__class__.__name__}{{ \"calledDateTime\": \"{called_date_time}\", "
                f"\"isConsumable\": \"{self._is_consumable}\", "
                f"\"isStateful\": \"{self._is_stateful}\", "
                f"\"isConsumed\": \"{self._is_consumed}\" }}")

    def consume(self) -> bool:
        """
        Mark the dispatch as having been consumed. If the dispatch is not consumable
        or has already been marked as consumed, returns False. Otherwise, returns True.

        Returns:
            bool: True if dispatch was consumed, False otherwise
        """
        if self._is_consumable and not self._is_consumed:
            self._is_consumed = True
            return True

        return False

    def get_called_date_time(self) -> datetime:
        """
        Return time the dispatch was marked valid.

        Returns:
            datetime: The datetime when the dispatch was marked valid
        """
        return self._called_date_time

    def get_results(self) -> Any:
        """
        Return any results stored in dispatch. If dispatch is stateful, this can be
        multiple results, otherwise it will be None or a single result.

        Returns:
            Any: The results stored in the dispatch
        """
        if len(self._results) < 1:
            return None

        return self._results

    @abstractmethod
    def initialize(self, input_data: Any) -> None:
        """
        Abstract method that handles initialization. Should mark dispatch as valid if
        successful, otherwise dispatch won't be usable with ChainHelper objects.

        Args:
            input_data: Initialization data for dispatch
        """
        pass

    def is_consumable(self) -> bool:
        """
        Return whether dispatch can be marked as consumed. If toggled and consumed,
        a ChainHelper will refuse to further distribute the dispatch.

        Returns:
            bool: True if dispatch can be consumed, False otherwise
        """
        return self._is_consumable

    def is_consumed(self) -> bool:
        """
        Return whether dispatch has been marked as consumed. If consumed, a ChainHelper
        will refuse to further distribute the dispatch.

        Returns:
            bool: True if dispatch has been consumed, False otherwise
        """
        return self._is_consumed

    def is_stateful(self) -> bool:
        """
        Return whether dispatch will hold multiple results during processing.

        Returns:
            bool: True if dispatch is stateful, False otherwise
        """
        return self._is_stateful

    def is_valid(self) -> bool:
        """
        Return whether dispatch is considered valid for processing by nodes.

        Returns:
            bool: True if dispatch is valid, False otherwise
        """
        return self._is_valid

    def make_consumable(self) -> 'DispatchBase':
        """
        Set dispatch as consumable.

        Returns:
            DispatchBase: Self for method chaining
        """
        self._is_consumable = True
        return self

    def make_stateful(self) -> 'DispatchBase':
        """
        Set dispatch as stateful.

        Returns:
            DispatchBase: Self for method chaining
        """
        self._is_stateful = True
        return self

    def make_valid(self) -> 'DispatchBase':
        """
        Set dispatch as valid and record the current date and time in UTC offset.

        Returns:
            DispatchBase: Self for method chaining
        """
        self._called_date_time = datetime.now(timezone.utc)
        self._is_valid = True
        return self

    def num_results(self) -> int:
        """
        Return number of results stored in dispatch.

        Returns:
            int: Number of results stored
        """
        return len(self._results)

    def set_result(self, result: Any) -> 'DispatchBase':
        """
        Set a result in dispatch. If dispatch is stateful, result is added to array,
        otherwise it replaces any existing results.

        Args:
            result: Result data to store in dispatch

        Returns:
            DispatchBase: Self for method chaining
        """
        if not self._is_stateful:
            self._results = [result]
        else:
            self._results.append(result)

        return self