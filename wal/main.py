from pathlib import Path

from .wal import WAL
from parser.parser import TLDBParser
from parser.transformer import TLDBParserTransformer

if __name__ == "__main__":
  wal = WAL(capacity = 0.0001) # 100 bytes capacity
  with open(Path(__file__).parent / "../parser/tldb.grammar.lark", "r") as f:
    grammar = f.read()
   
  while True:
    stdin = input(">>> ")
    tree = TLDBParser.parser(grammar).parse(stdin)
    _, log = TLDBParserTransformer().transform(tree)
    wal.row(log, safe = True)