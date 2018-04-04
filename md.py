import sys
import argparse
from parser import Parser

optParser = argparse.ArgumentParser()
optParser.add_argument('name', help = '歌名+歌手名,空格隔开')
optParser.add_argument('-n', help = '歌名+歌手名,空格隔开', dest = 'name')

args = optParser.parse_args()
name = args.name

parser = Parser()
parser.start(name)