#!/usr/bin/env python
"""
2018-12-13 19:57:40
@author: Paul Reiter
"""
from parse import parse
from itertools import chain, tee


def parse_line(line):
    return tuple(parse('Step {} must be finished before step {} can begin.',
                       line))


def link(node1, node2):
    node1.children.add(node2)
    node2.parents.add(node1)


def replace_with_children(node_set, node):
    """Replaces `node` in set() `node_set` with its children"""
    node_set.remove(node)
    node_set = node_set.union(node.children)
    return node_set


def time_of_task(letter, offset=60):
    return ord(letter) - 64 + offset


class Node:

    def __init__(self, value):
        self.value = value
        self.parents, self.children = set(), set()

    def __repr__(self):
        child_values = sorted(child.value for child in self.children)
        parent_values = sorted(parent.value for parent in self.parents)
        return (f"Node(value='{self.value}', parents={parent_values}, "
                f"children={child_values})")

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value


class Tree:

    def __init__(self, node_names):
        self.nodes = {}
        for node_name in node_names:
            self.nodes[node_name] = Node(node_name)

    def link(self, relation):
        link(self.nodes[relation[0]], self.nodes[relation[1]])

    def link_all(self, relations):
        for relation in relations:
            self.link(relation)

    @property
    def heads(self):
        return set(node for node in self.nodes.values()
                   if len(node.parents) == 0)

    @property
    def tails(self):
        return set(node for node in self.nodes.values()
                   if len(node.children) == 0)

    @classmethod
    def from_relations(cls, relations):
        rel1, rel2 = tee(relations)
        tree = cls(set(chain.from_iterable(relation for relation in rel1)))
        tree.link_all(rel2)
        return tree

    @classmethod
    def from_lines(cls, lines):
        return cls.from_relations(parse_line(line) for line in lines)

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'r') as stream:
            lines = stream.readlines()
        return cls.from_lines(lines)

    def __iter__(self):
        done = set()
        while len(done) < len(self.nodes):
            available = set(node for node in self.nodes.values()
                            if all(parent in done for parent in node.parents)
                            and node not in done)
            step = sorted(available)[0]
            done.add(step)
            yield step

    def async_iter(self, num_workers, offset=60):
        done = []
        time = 0
        workers = [Worker() for _ in range(num_workers)]
        progress = set()
        while len(done) < len(self.nodes):
            # move finished tasks to `done`
            for worker in workers:
                if worker.done:
                    if worker.task in self.nodes:
                        done.append(self.nodes[worker.task])
                        progress.remove(self.nodes[worker.task])
            # find available tasks
            available = [node for node in self.nodes.values()
                         if all(parent in done for parent in node.parents)
                         and node not in done and node not in progress]
            available.sort(reverse=True)
            # distribute available tasks to workers
            for worker in workers:
                if worker.done:
                    if len(available) == 0:
                        break
                    task = available.pop()
                    progress.add(task)
                    worker.add_task(task.value,
                                    time_of_task(task.value, offset=offset))
            # yield time and tasks of all workers
            done_string = (''.join(ele.value for ele in done)
                           if len(done) > 0 else '.')
            yield (time, *(worker.next() for worker in workers), done_string)
            time += 1


class Worker:

    def __init__(self):
        self.task = '.'
        self.time = 0

    def next(self):
        if self.time > 0:
            self.time -= 1
            return self.task
        self.task = '.'
        return self.task

    @property
    def done(self):
        return self.time <= 0

    def add_task(self, task, time):
        self.task = task
        self.time = time

    def __repr__(self):
        return f"Worker(task='{self.task}', time='{self.time})'"


if __name__ == '__main__':
    tree = Tree.from_file('input_07.txt')
    print(''.join(node.value for node in tree))
    tree = Tree.from_file('input_07.txt')
    async_iter = tree.async_iter(5)
    with open('output_07.txt', 'w') as stream:
        for time_step in async_iter:
            stream.write(str(time_step) + '\n')
