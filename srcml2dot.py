#!/usr/bin/python3

from bs4 import BeautifulSoup
from html.parser import HTMLParser

import multiprocessing
import pickle
import networkx as nx
import re
import statistics
import numpy as np
import sys

from networkx.drawing.nx_agraph import write_dot

if len(sys.argv) < 3:
    print('USAGE: srcml2dot.py INPUT.srcml OUTPUT.dot')
    quit()

infile = sys.argv[1]
outfile = sys.argv[2]

def re_0002(i):
    # split camel case and remove special characters
    tmp = i.group(0)
    if len(tmp) > 1:
        if tmp.startswith(' '):
            return tmp
        else:
            return '{} {}'.format(tmp[0], tmp[1])
    else:
        return ' '.format(tmp)

re_0001_ = re.compile(r'([^a-zA-Z0-9 ])|([a-z0-9_][A-Z])')

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super(MyHTMLParser, self).__init__()
        self.parentstack = list()
        self.curtag = -1
        self.tagidx = -1
        self.graph = nx.Graph()
        self.seq = list()
        
    def handle_starttag(self, tag, attrs):
        self.parentstack.append(self.curtag)
        self.tagidx += 1
        self.seq.append(tag)
        self.graph.add_node(self.tagidx, label=tag)
        if self.parentstack[-1] >= 0:
            self.graph.add_edge(self.parentstack[-1], self.tagidx)
        self.curtag = self.tagidx
        
    def handle_endtag(self, tag):
        self.curtag = self.parentstack.pop()
        
    def handle_data(self, data):
        
        # first, do dats text preprocessing
        data = re_0001_.sub(re_0002, data).lower().rstrip()
        
        # second, create a node if there is text
        if(data != ''):
            for d in data.split(' '): # each word gets its own node
                if d != '':
                    self.parentstack.append(self.curtag)
                    self.tagidx += 1
                    self.seq.append(d)
                    self.graph.add_node(self.tagidx, label=d, fontname='times-bold')
                    self.graph.add_edge(self.parentstack[-1], self.tagidx)
                    self.curtag = self.tagidx
                    self.curtag = self.parentstack.pop()
        
    def get_graph(self):
        return(self.graph)

    def get_seq(self):
        return(self.seq)

c = 0

def xmldecode(unit):
    parser = MyHTMLParser()
    parser.feed(unit)
    return(parser.get_graph(), parser.get_seq())

with open(infile, 'r') as f:
    unit = f.read()

(graph, seq) = xmldecode(unit)

write_dot(graph, outfile)

print(seq)

