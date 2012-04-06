#!/usr/bin/env python

import to_from

def main(args):
    args.remove(args[0])
    for file_name in args:
        fp = open(file_name, 'rb')
        fp_target = open(file_name + '.csv', 'wb')
        data_as_list = to_from.fp_to_list(fp)
        to_from.list_to_csv(data_as_list, fp_target)
        fp.close()
        fp_target.close()


if __name__ == '__main__':
    import sys
    main(sys.argv)
