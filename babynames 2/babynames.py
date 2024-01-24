#!/usr/bin/env python3

"""
Stanford CS106A BabyNames Project
Part-A: organizing the bulk data
"""

import sys

YEARS = [1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000,
         2010, 2020]
def add_name(names, year, rank, name):
    """
    Add the given data: int year, int rank, string name
    to the given names dict and return it.
    (1 test provided, more tests TBD)
    >>> add_name({}, 2000, 10, 'Abe')
    {'Abe': {2000: 10}}
    >>> # Student Tests Here (keep this line)
    >>> add_name({}, 2001, 10, 'Abe')
    {'Abe': {2001: 10}}
    >>> add_name({}, 2000, 11, 'Abe')
    {'Abe': {2000: 11}}
    >>> add_name({}, 2000, 9, 'john')
    {'john': {2000: 9}}
    """

    if name not in names:
        names[name] = {}
    years = names[name]
    if year not in years:
        years[year] = 0
    else:
        return names
    years[year] = rank

    return names



def parse_year(filename):
    """
    Given filename, like 'baby-2000.txt'
    extract and return the int year from between
    the dash and the dot, e.g. 2000
    Raises an exception on failure.
    (Tests provided)
    >>> parse_year('baby-2000.txt')
    2000
    >>> parse_year('infant-123.txt')
    123
    >>> parse_year('nope123.txt')  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    Exception:...
    """

    first = filename.find('-')
    last = filename.find('.')
    if first != -1 and last != -1:
        year = int(filename[first + 1:last])
    else:
        raise Exception('Cannot parse filename:' + filename)

    return year


def add_file(names, filename):
    """
    Given a names dict and filename like baby-2000.txt,
    add the file's data to the dict and return it.
    (Tests provided, Code TBD)
    >>> add_file({}, 'small-2000.txt')
    {'Bob': {2000: 1}, 'Alice': {2000: 1}, 'Cindy': {2000: 2}}
    >>> add_file({}, 'small-2010.txt')
    {'Yot': {2010: 1}, 'Zena': {2010: 1}, 'Bob': {2010: 2}, 'Alice': {2010: 2}}
    >>> # Names non-empty, add small-2010.txt to it
    >>> add_file({'Bob': {2000: 1}, 'Alice': {2000: 1}, 'Cindy': {2000: 2}}, 'small-2010.txt')
    {'Bob': {2000: 1, 2010: 2}, 'Alice': {2000: 1, 2010: 2}, 'Cindy': {2000: 2}, 'Yot': {2010: 1}, 'Zena': {2010: 1}}
    """

    year = parse_year(filename)
    with open(filename) as f:
        for line in f:
            line = line.strip()
            words = line.split()

            parts = line.split(',')
            rank = int(parts[0])
            name = parts[1]

            add_name(names, year, rank, name)
            name = parts[2]

            add_name(names, year, rank, name)

    return names


def read_files(filenames):
    """
    Given list of filenames, build and return a names dict
    of all their data.
    >>> read_files(['small-2000.txt', 'small-2010.txt'])
    {'Bob': {2000: 1, 2010: 2}, 'Alice': {2000: 1, 2010: 2}, 'Cindy': {2000: 2}, 'Yot': {2010: 1}, 'Zena': {2010: 1}}
    """
    names = {}
    for filename in filenames:
        add_file(names, filename)

    return names


def search_names(names, target):
    """
    Given names dict and a target string,
    return a sorted list of all the name strings
    that contain that target string anywhere.
    Not case sensitive.
    (Code and tests TBD)
    >>> # Student Tests Here (keep this line)
    >>> search_names({'drake', 'kanye'}, 'k')
    ['drake', 'kanye']
    >>> search_names({'drake', 'kanye'}, 'ke')
    ['drake']
    >>> search_names({'drake', 'kanye'}, 'kylie')
    []
    """
    lst = []
    for name in names:
        if target in name:
            lst.append(name)
            lst = sorted(lst)
    return lst



def print_names(names):
    """
    (provided)
    Given names dict, print out all its data, one name per line.
    The names are printed in increasing alphabetical order,
    with its years data also in increasing order, like:
    Aaden [(2010, 560)]
    Aaliyah [(2000, 211), (2010, 56)]
    ...
    Surprisingly, this can be done with 2 lines of code.
    We'll explore this in lecture.
    """
    for key, value in sorted(names.items()):
        print(key, sorted(value.items()))


def main():
    # (provided)
    args = sys.argv[1:]
    # Two command line forms
    # 1. file1 file2 file3 ..
    # 2. -search target file1 file2 file3 ..

    # Assume no search, so list of filenames to read
    # is the args list
    filenames = args

    # Check if we are doing search, set target variable
    target = ''
    if len(args) >= 2 and args[0] == '-search':
        target = args[1]
        filenames = args[2:]  # Change filenames to skip first 2

    # Read in all the filenames: baby-1990.txt, baby-2000.txt, ...
    names = read_files(filenames)

    # Either we do a search or just print everything.
    if target != '':
        search_results = search_names(names, target)
        for name in search_results:
            print(name)
    else:
        print_names(names)


if __name__ == '__main__':
    main()
