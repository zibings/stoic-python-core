from .node_base import NodeBase
from .dispatch_base import DispatchBase
from typing import List, Any, Optional, Dict, Callable


class ChainHelper:
    """
    Class to maintain groups (chains) of nodes and send events to them.
    """

    def __init__(self, is_event: bool = False, do_debug: bool = False):
        """
        Create a new instance of ChainHelper class. If set as an event-chain,
        only one node may be linked to chain at any given time.

        Args:
            is_event: Toggle for event-chain
            do_debug: Toggle for sending debug messages
        """
        self._nodes: List[NodeBase] = []
        self._is_event: bool = is_event
        self._do_debug: bool = False
        self._logger: Optional[Callable[[str], None]] = None

        self.toggle_debug(do_debug)

    def toggle_debug(self, do_debug: bool) -> 'ChainHelper':
        """
        Toggle the use of debug messages by this instance.

        Args:
            do_debug: Toggle for sending debug messages

        Returns:
            ChainHelper: Self for method chaining
        """
        self._do_debug = do_debug
        return self

    def get_node_list(self) -> List[Dict[str, str]]:
        """
        Return the full list of nodes linked to the chain.

        Returns:
            List[Dict[str, str]]: List of node information
        """
        ret = []

        for node in self._nodes:
            ret.append({
                'key': node.get_key(),
                'version': node.get_version()
            })

        return ret

    def hook_logger(self, callback: Callable[[str], None]) -> None:
        """
        Attach the given callback to the chain to receive debug messages, if enabled.
        Callbacks should accept a single string argument.

        Args:
            callback: Callable method/function that receives messages
        """
        self._logger = callback

    def is_event(self) -> bool:
        """
        Return whether chain is set up as an event-chain.

        Returns:
            bool: True if chain is an event-chain, False otherwise
        """
        return self._is_event

    def link_node(self, node: NodeBase) -> 'ChainHelper':
        """
        Register a NodeBase object with the chain. If chain is an event-chain,
        this will overwrite any existing node. If node is invalid, link will fail.

        Args:
            node: NodeBase object to register with chain

        Returns:
            ChainHelper: Self for method chaining
        """
        if not node.is_valid():
            if self._do_debug:
                self.log(f"Attempted to add invalid node: {node}")

            return self

        if self._is_event:
            if self._do_debug:
                self.log(f"Setting event node: {node}")

            self._nodes = [node]
        else:
            if self._do_debug:
                self.log(f"Linking new node: {node}")

            self._nodes.append(node)

        return self

    def traverse(self, dispatch: DispatchBase, sender: Any = None) -> bool:
        """
        Trigger distribution of given dispatch to all linked nodes in chain.
        Will return False if no nodes are linked, the dispatch is invalid,
        or the dispatch is consumable and has already been consumed.

        Args:
            dispatch: DispatchBase object to distribute to linked nodes
            sender: Optional sender data to pass to linked nodes

        Returns:
            bool: True if traversal was successful, False otherwise
        """
        if len(self._nodes) < 1:
            if self._do_debug:
                self.log("Attempted to traverse chain with no nodes")

            return False

        if not dispatch.is_valid():
            if self._do_debug:
                self.log(f"Attempted to traverse chain with invalid dispatch: {dispatch}")

            return False

        if dispatch.is_consumable() and dispatch.is_consumed():
            if self._do_debug:
                self.log(f"Attempted to traverse chain with consumed dispatch: {dispatch}")

            return False

        if sender is None:
            sender = self

        is_consumable = dispatch.is_consumable()

        if self._is_event:
            if self._do_debug:
                self.log(f"Sending dispatch ({dispatch}) to event node: {self._nodes[0]}")

            self._nodes[0].process(sender, dispatch)
        else:
            for i, node in enumerate(self._nodes):
                if self._do_debug:
                    self.log(f"Sending dispatch ({dispatch}) to node: {node}")

                node.process(sender, dispatch)

                if is_consumable and dispatch.is_consumed():
                    if self._do_debug:
                        self.log(f"Dispatch ({dispatch}) consumed by node: {node}")

                    break

        return True

    def log(self, message: str) -> None:
        """
        Conditionally send debug message to registered callback.

        Args:
            message: Message to send to callback
        """
        if self._logger is not None:
            self._logger(message)