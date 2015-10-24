'''
Created on 16 oct. 2015

@author: Antonin Duroy
'''
from collections import OrderedDict

def insert_at_position(iterable, position, new_item):
    """ Insert an item at a certain position in a Python OrderedDict an return
    a new OrderedDict
    """
    if len(new_item) != 2:
        raise ValueError('new_item must be of length 2.')
    items = []
    inserted = False
    for i, item in enumerate(iterable.items()):
        if i != position:
            items.append(item)
        else:
            items.append(new_item)
            items.append(item)
            inserted = True
    if not inserted:
        items.append(new_item)
    return OrderedDict(items)