#!/usr/bin/env python3
"""
2018-12-25 09:00:24
@author: Paul Reiter
"""


class Node:

    def __init__(self, n_children):
        self.n_children = n_children
        self.metadata = None
        self.children = []
        self._value = None

    def add_child(self, child_node):
        if len(self.children) < self.n_children:
            self.children.append(child_node)
        else:
            raise ValueError('Can not append more child nodes!')

    @classmethod
    def from_list(cls, list_):
        n_children = list_[0]
        n_metadata_entries = list_[1]
        if not n_children:
            node = cls(n_children)
            length = 2+n_metadata_entries
            node.metadata = tuple(list_[2:length])
            return node, list_[length:]
        else:
            remaining_list = list_[2:]
            node = cls(n_children)
            for n in range(n_children):
                child_node, remaining_list = cls.from_list(remaining_list)
                node.add_child(child_node)
            node.metadata = tuple(remaining_list[:n_metadata_entries])
            return node, remaining_list[n_metadata_entries:]

    def sum_metadata(self):
        return (sum(self.metadata) +
                sum(child.sum_metadata() for child in self.children))

    @property
    def value(self):
        if self._value is None:
            if len(self.children) == 0:
                self._value = sum(self.metadata)
            else:
                self._value = 0
                for index in self.metadata:
                    try:
                        self._value += self.children[index-1].value
                    except IndexError:
                        pass
        return self._value


if __name__ == '__main__':
    with open('input_08.txt', 'r') as stream:
        content = [int(ele) for ele in stream.readline().split()]
    root, remaining_list = Node.from_list(content)
    print(f'The sum of all metadata entries is: {root.sum_metadata()}')
    print(f'The value of the root node is: {root.value}')
