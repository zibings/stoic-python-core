from typing import List, Any


class ReturnHelper:
    """
    Class to provide more data for method/function returns.

    This class helps manage function returns with status indicators,
    messages, and multiple results.
    """

    # Status constants
    STATUS_BAD = 0
    STATUS_GOOD = 1

    def __init__(self):
        """
        Instantiates a new ReturnHelper class. Default status is STATUS_BAD.
        """
        self._messages = []  # type: List[str]
        self._results = []  # type: List[Any]
        self._status = self.STATUS_BAD

    def add_message(self, message: str) -> None:
        """
        Adds a message onto the internal collection.

        Args:
            message: String value of message to add to collection.
        """
        self._messages.append(message)

    def add_messages(self, messages: List[str]) -> None:
        """
        Adds a group of messages onto the internal collection.

        Args:
            messages: List of strings to add to collection.

        Raises:
            ValueError: If messages list is empty.
        """
        if len(messages) < 1:
            raise ValueError("Messages list to add_messages() must be a list with elements")

        for msg in messages:
            self._messages.append(msg)

    def add_result(self, result: Any) -> None:
        """
        Adds a result onto the internal collection.

        Args:
            result: Result value to add to collection.
        """
        self._results.append(result)

    def add_results(self, results: List[Any]) -> None:
        """
        Adds a group of results onto the internal collection.

        Args:
            results: List of results to add to collection.

        Raises:
            ValueError: If results list is empty.
        """
        if len(results) < 1:
            raise ValueError("Results list to add_results() must be a list with elements")

        for res in results:
            self._results.append(res)

    def is_bad(self) -> bool:
        """
        Returns TRUE if the current internal status is set to STATUS_BAD.

        Returns:
            bool: True if status is bad, False otherwise.
        """
        return self._status == self.STATUS_BAD

    def is_good(self) -> bool:
        """
        Returns TRUE if the current internal status is set to STATUS_GOOD.

        Returns:
            bool: True if status is good, False otherwise.
        """
        return self._status == self.STATUS_GOOD

    def get_messages(self) -> List[str]:
        """
        Returns the internal collection of messages.

        Returns:
            List[str]: List of stored messages.
        """
        return self._messages

    def get_results(self) -> List[Any]:
        """
        Returns the internal collection of results.

        Returns:
            List[Any]: List of stored results.
        """
        return self._results

    def has_messages(self) -> bool:
        """
        Returns TRUE if there are messages stored in the internal collection.

        Returns:
            bool: True if messages exist, False otherwise.
        """
        return len(self._messages) > 0

    def has_results(self) -> bool:
        """
        Returns TRUE if there are results stored in the internal collection.

        Returns:
            bool: True if results exist, False otherwise.
        """
        return len(self._results) > 0

    def make_bad(self) -> None:
        """
        Sets the internal status as STATUS_BAD.
        """
        self._status = self.STATUS_BAD

    def make_good(self) -> None:
        """
        Sets the internal status as STATUS_GOOD.
        """
        self._status = self.STATUS_GOOD