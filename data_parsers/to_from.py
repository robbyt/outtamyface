#!/usr/bin/env python

import csv
import cPickle as pickle

class Unknown_input(Exception):
    pass

def fp_to_list(fp, split_type=' '):
    """ Pass in a filepointer, and optionally a split type, and this will read
        your file, and return back a parsed list
    """
    if type(fp) is file:
        return [row.split(split_type) for row in fp.read().splitlines()]
        return fp
    else:
        raise Unknown_input

def fp_to_list_gennerator(fp, split_type=' '):
    """ Similar to to_list(), but this function acts as a gennerator to return
        a single row at a time.
    """
    if type(fp) is file:
        yield [row.split(split_type) for row in fp.readline()]
        return fp
    else:
        raise Unknown_input

def list_to_pickle(list_data, fp_target, protocol=2):
    pickle.dump(list_data, fp_target, protocol=protocol)
    return fp_target

def pickle_to_list(fp_target):
    return pickle.load(fp_target)

def list_to_csv(list_data, fp_target):
    """ Pass in a big list of data, or a gennerator
    """
    write = csv.writer(fp_target)
    list_data_type = type(list_data)

    if list_data_type is list:
        for row in list_data:
            write.writerow(row)
        return fp_target

    elif list_data_type is function:
        for row in list_data():
            write.writerow(row)
        return fp_target

    else:
        raise Unknown_input("Error reading list_data, found type: " + str(list_data_type))
        
 
