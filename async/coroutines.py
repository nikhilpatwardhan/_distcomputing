#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 04:07:21 2016

@author: nikhil
"""

def coroutine(fn):
    def wrapper(*args, **kwargs):
        c = fn(*args, **kwargs)
        next(c)
        return c
    return wrapper

def cat(f, case_insensitive, child):
    '''
    This is where execution begins
    The child here is the grep coroutine
    '''
    if case_insensitive:
        line_processor = lambda l: l.lower()
    else:
        line_processor = lambda l: l
    
    for line in f:
        child.send(line_processor(line))

@coroutine
def grep(substring, case_insensitive, child):
    '''
    The child here is count coroutine
    '''
    if case_insensitive:
        substring = substring.lower()
    
    while True:
        text = (yield)
        child.send(text.count(substring))   # The actual work is done by
                                            # Python's string class

@coroutine
def count(substring):
    '''
    Just an accumulator of counts, maintains a running total
    '''
    n = 0
    try:
        while True:
            n += (yield)
    except GeneratorExit:
        print(substring, n)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='store_true', dest='case_insensitive')
    parser.add_argument('pattern', type=str)
    parser.add_argument('infile', type=argparse.FileType('r'))
    args = parser.parse_args()
    
    cat(args.infile, args.case_insensitive, \
        grep(args.pattern, args.case_insensitive, count(args.pattern)))