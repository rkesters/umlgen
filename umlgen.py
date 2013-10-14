#!/usr/bin/python

import argparse















if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create Sequence')
    parser.add_argument('path', type=str , help="path to source directory")
    args = parser.parse_args()
    print args.path
