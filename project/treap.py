from collections.abc import MutableMapping
from typing import Optional, Iterator, Tuple
import random


class Node:
    """
    Узел для декартова дерева.

    Attributes:
        key: Ключ узла.
        value: Значение узла.
        priority: Приоритет узла для поддержания кучи.
        left: Левый дочерний узел.
        right: Правый дочерний узел.
    """

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.priority = random.randint(0, 100)
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None


class Treap(MutableMapping):
    """
    Реализация декартова дерева (Treap) с поддержкой словарного интерфейса.

    Methods:
        __setitem__(self, key, value): Вставка или обновление значения по ключу.
        __getitem__(self, key): Получение значения по ключу.
        __delitem__(self, key): Удаление элемента по ключу.
        __contains__(self, key): Проверка наличия ключа.
        __iter__(self): Прямой обход ключей.
        __reversed__(self): Обратный обход ключей.
    """

    def __init__(self):
        self.root: Optional[Node] = None

    def _split(
        self, node: Optional[Node], key
    ) -> Tuple[Optional[Node], Optional[Node]]:
        """
        Разделяет дерево на две части: те, у которых ключ меньше key и те, у которых больше или равен key.
        """
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
        Объединяет два дерева с сохранением свойств кучи.
        """
        if not left or not right:
            return left or right
        elif left.priority > right.priority:
            left.right = self._merge(left.right, right)
            return left
        else:
            right.left = self._merge(left, right.left)
            return right

    def __setitem__(self, key, value):
        """
        Вставка или обновление значения по ключу.
        """

        def insert(node: Optional[Node], key, value) -> Node:
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

    def __getitem__(self, key):
        """
        Получение значения по ключу.
        """
        node = self._find(self.root, key)
        if node is None:
            raise KeyError(f"Key {key} not found")
        return node.value

    def __delitem__(self, key):
        """
        Удаление элемента по ключу.
        """

        def delete(node: Optional[Node], key) -> Optional[Node]:
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

    def __contains__(self, key) -> bool:
        """
        Проверка наличия ключа в дереве.
        """
        return self._find(self.root, key) is not None

    def __iter__(self) -> Iterator:
        """
        Прямой обход дерева.
        """
        yield from self._inorder(self.root)

    def __reversed__(self) -> Iterator:
        """
        Обратный обход дерева.
        """
        yield from self._reverse_inorder(self.root)

    def _inorder(self, node: Optional[Node]) -> Iterator:
        """
        Внутренний метод для прямого обхода.
        """
        if node is not None:
            yield from self._inorder(node.left)
            yield node.key
            yield from self._inorder(node.right)

    def _reverse_inorder(self, node: Optional[Node]) -> Iterator:
        """
        Внутренний метод для обратного обхода.
        """
        if node is not None:
            yield from self._reverse_inorder(node.right)
            yield node.key
            yield from self._reverse_inorder(node.left)

    def _find(self, node: Optional[Node], key) -> Optional[Node]:
        """
        Поиск узла по ключу.
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
        Правый поворот для поддержания свойств дерева.
        """
        new_root = node.left
        node.left = new_root.right
        new_root.right = node
        return new_root

    def _rotate_left(self, node: Node) -> Node:
        """
        Левый поворот для поддержания свойств дерева.
        """
        new_root = node.right
        node.right = new_root.left
        new_root.left = node
        return new_root

    def __len__(self) -> int:
        """
        Подсчет количества узлов.
        """
        return sum(1 for _ in self)
