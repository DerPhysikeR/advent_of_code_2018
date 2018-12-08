#!/usr/bin/env python
"""
2018-12-07 21:11:04
@author: Paul Reiter
"""
from datetime import datetime, timedelta
from operator import itemgetter
from collections import namedtuple, defaultdict


Line = namedtuple('Line', 'time action')


def parse_line(line):
    """Parse one line of the input file"""
    return Line(datetime.fromisoformat(line[1:17]), line[19:].rstrip())


def shifts(data):
    """Separates data into individual shifts"""
    start = 0
    for line_number, line in enumerate(data[1:], 1):
        if 'Guard' in line.action:
            end = line_number
            yield data[start:end]
            start = line_number
    yield(data[start:])


def get_guard_id(action):
    return int(action.partition('#')[2].partition(' ')[0])


def minuterator(timestamp1, timestamp2):
    time = timestamp1
    while time < timestamp2:
        yield time.time()
        time += timedelta(minutes=1)


if __name__ == '__main__':
    # read and sort data
    with open('input_04.txt', 'r') as stream:
        data = [parse_line(line) for line in stream.readlines()]
    data.sort(key=itemgetter(0))

    # sum sleeping time for each guard
    time_asleep = defaultdict(int)
    sleepiest_patterns = []
    for shift in shifts(data):
        guard_id = get_guard_id(shift[0].action)
        asleep = sum((end.time - start.time).seconds//60 for start, end
                     in zip(shift[1::2], shift[2::2]))
        time_asleep[guard_id] += asleep
        if guard_id == 971:
            sleepiest_patterns.extend([s.time for s in shift[1:]])

    # print laziest guard
    max_sleeping_time = max(time_asleep.values())
    for guard_id, sleeping_time in time_asleep.items():
        if sleeping_time == max_sleeping_time:
            print(f'guard id: {guard_id}')
            print(f'sleeping time: {sleeping_time}')

    # find minute when the guard is asleep the most
    slept_minutes = defaultdict(int)
    for start, end in zip(sleepiest_patterns[::2], sleepiest_patterns[1::2]):
        for minute in minuterator(start, end):
            slept_minutes[minute] += 1

    # print most slept minute
    max_sleep_count = max(slept_minutes.values())
    for minute, sleep_count in slept_minutes.items():
        if sleep_count == max_sleep_count:
            print(minute)
            print(sleep_count)

    print(971*38)
