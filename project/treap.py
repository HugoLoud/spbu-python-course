from collections.abc import MutableMapping
from typing import Optional, Iterator, Tuple
import random


class Node:
    """
    Node for the treap (Cartesian tree).

    Attributes:
        key: The key of the node.
        value: The value of the node.
        priority: The priority of the node for maintaining heap properties.
        left: The left child node.
        right: The right child node.
    """

    def __init__(self, key: int, value: str) -> None:
        self.key = key
        self.value = value
        self.priority = random.randint(0, 100)
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None


class Treap:
    """
    Implementation of a treap (Cartesian tree) with dictionary-like interface.

    Methods:
        __setitem__(self, key, value): Insert or update a value by key.
        __getitem__(self, key): Retrieve a value by key.
        __delitem__(self, key): Remove an item by key.
        __contains__(self, key): Check if a key exists in the treap.
        __iter__(self): Iterate through keys in ascending order.
        __reversed__(self): Reverse iteration over keys.
        split(self, root, key): Split the treap into two parts by a key.
        merge(self, left, right): Merge two treaps.
    """

    def __init__(self) -> None:
        self.root: Optional[Node] = None

    def _split(
        self, node: Optional[Node], key: int
    ) -> Tuple[Optional[Node], Optional[Node]]:
        """
        Splits the treap into two subtrees.

        Args:
            node: The root node of the treap to split.
            key: The key to split by.

        Returns:
            A tuple containing two subtrees.
        """
        left: Optional[Node] = None
        right: Optional[Node] = None

        if node is None:
            return None, None
        elif key > node.key:
            left, node.right = self._split(node.right, key)
            node.right = left
            return node, right
        else:
            node.left, right = self._split(node.left, key)
            node.left = right
            return left, node

    def _merge(self, left: Optional[Node], right: Optional[Node]) -> Optional[Node]:
        """
        Merges two treaps into one.

        Args:
            left: The root of the left treap.
            right: The root of the right treap.

        Returns:
            The root of the merged treap.
        """
        if left is None or right is None:
            return left or right
        elif left.priority > right.priority:
            left.right = self._merge(left.right, right)
            return left
        else:
            right.left = self._merge(left, right.left)
            return right

    def __setitem__(self, key: int, value: str) -> None:
        """
        Inserts or updates a node with the given key and value.

        Args:
            key (int): The key of the node.
            value (str): The value of the node.
        """

        def insert(node: Optional[Node], key: int, value: str) -> Node:
            if node is None:
                return Node(key, value)
            if key == node.key:
                node.value = value
            elif key < node.key:
                node.left = insert(node.left, key, value)
                if node.left and node.left.priority > node.priority:
                    node = self._rotate_right(node)
            else:
                node.right = insert(node.right, key, value)
                if node.right and node.right.priority > node.priority:
                    node = self._rotate_left(node)
            return node

        self.root = insert(self.root, key, value)

    def __getitem__(self, key: int) -> str:
        """
        Retrieves the value associated with a key.

        Args:
            key (int): The key to retrieve the value for.

        Returns:
            str: The value associated with the key.

        Raises:
            KeyError: If the key is not found in the treap.
        """
        node = self._find(self.root, key)
        if node is None:
            raise KeyError(f"Key {key} not found")
        return node.value

    def __delitem__(self, key: int) -> None:
        """
        Removes a key-value pair from the treap.

        Args:
            key (int): The key to remove.

        Returns:
            None

        Raises:
            KeyError: If the key does not exist.
        """

        def delete(node: Optional[Node], key: int) -> Optional[Node]:
            if node is None:
                raise KeyError(f"Key {key} not found")
            if key < node.key:
                node.left = delete(node.left, key)
            elif key > node.key:
                node.right = delete(node.right, key)
            else:
                node = self._merge(node.left, node.right)
            return node

        self.root = delete(self.root, key)

    def __contains__(self, key: int) -> bool:
        """
        Checks whether a key exists in the treap.

        Args:
            key (int): The key to check.

        Returns:
            bool: True if the key exists, False otherwise.
        """
        return self._find(self.root, key) is not None

    def __iter__(self) -> Iterator[int]:
        """
        Performs an in-order traversal of the treap.

        Returns:
            Iterator[int]: Iterator over the keys in ascending order.
        """
        yield from self._inorder(self.root)

    def __reversed__(self) -> Iterator[int]:
        """
        Performs a reverse in-order traversal of the treap.

        Returns:
            Iterator[int]: Iterator over the keys in descending order.
        """
        yield from self._reverse_inorder(self.root)

    def _inorder(self, node: Optional[Node]) -> Iterator[int]:
        """
            Performs an in-order traversal of the treap.

        Args:
            node (Optional[Node]): The root node of the current subtree.

        Yields:
            int: Keys in ascending order.
        """
        if node is not None:
            yield from self._inorder(node.left)
            yield node.key
            yield from self._inorder(node.right)

    def _reverse_inorder(self, node: Optional[Node]) -> Iterator[int]:
        """
        Performs a reverse in-order traversal of the treap.

        Args:
            node (Optional[Node]): The root node of the current subtree.

        Yields:
            int: Keys in descending order.
        """
        if node is not None:
            yield from self._reverse_inorder(node.right)
            yield node.key
            yield from self._reverse_inorder(node.left)

    def _find(self, node: Optional[Node], key: int) -> Optional[Node]:
        """
        Searches for a node with the specified key in the treap.

        Args:
            node (Optional[Node]): The root node of the current subtree.
            key (int): The key to search for.

        Returns:
            Optional[Node]: The node with the specified key, or None if not found.
        """
        while node is not None:
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                return node
        return None

    def _rotate_right(self, node: Node) -> Node:
        """
        Performs a right rotation to restore heap properties.

        Args:
            node (Node): The root node to rotate.

        Returns:
            Node: The new root node after the rotation.
        """
        if node.left is None:
            return node
        new_root = node.left
        node.left = new_root.right
        new_root.right = node
        return new_root

    def _rotate_left(self, node: Node) -> Node:
        """
        Performs a left rotation to restore heap properties.

        Args:
            node (Node): The root node to rotate.

        Returns:
            Node: The new root node after the rotation.
        """
        if node.right is None:
            return node
        new_root = node.right
        node.right = new_root.left
        new_root.left = node
        return new_root

    def __len__(self) -> int:
        """
        Returns the number of nodes in the treap.

        Returns:
            int: The number of key-value pairs.
        """
        return sum(1 for _ in self)
