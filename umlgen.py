#!/usr/bin/python
import os
import argparse, ctags
from ctags import CTags, TagEntry
import mmap

tagFile = None
base = {}
def genTags(path):
    from subprocess import call
    call(["ctags", "--fields=afmikKlnsStz", path ])
    tagFile = CTags("tags")
    if tagFile is None:
        print "bad tagfile"
    return tagFile

def genUmlForFiles(path):
    for root, _, files in os.walk(path):
        for fn in files:
            f = os.path.join(root, fn)
            print f
            base[os.path.basename(f)] = { "path" : f}
            me = base[os.path.basename(f)]
            tagFile = genTags(f)
            entry = TagEntry()
            ne = TagEntry()
            status = tagFile.first(entry)
            if status:
                print "Tag: " + entry['name'] + " Status: " + str(status) +  "kind: " + str(entry['kind'])
                if entry['kind'] == 'function':
                    fh = open(f)
                    s = mmap.mmap(fh.fileno(), 0, access=mmap.ACCESS_READ)
                    lnr = entry['lineNumber']
                    print "Look for " + entry['name'] + " @ " + str(lnr)
                    loc = s.find(entry['name'], lnr)
                    if loc != -1:
                        print "found tag in file"
                        s.seek(loc)
                        ln = s.readline()
                        cnt = lnr
                        status = tagFile.next(ne)
                        stop = ne['lineNumber']
                        print "Tag: " + entry['name'] + " Stop Line: " + str(stop)
                        while cnt < stop and ln != None:
                            print ln
                            ln = s.readline()
                            cnt = cnt + 1
                            print "cnt : " + str(cnt)                
#                    me["functions"] = 
            break        
        break        



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create Sequence')
    parser.add_argument('path', type=str , help="path to source directory")
    parser.add_argument('--entry', type=str , help="comman seperate list of entry points")
    args = parser.parse_args()
    genUmlForFiles(args.path)
