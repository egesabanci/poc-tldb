from pathlib import Path

from .tldb_parser import TLDBParser
from .tldb_transformer import TLDBParserTransformer

if __name__ == "__main__":
  with open(Path(__file__).parent / "tldb.grammar.lark", "r", encoding = "UTF-8") as file:
    grammar = file.read()

  stdin = input(">>> ")
  parser = TLDBParser.parser(grammar)
  parsed = parser.parse(stdin)

  transformer = TLDBParserTransformer().transform(parsed)
  print(transformer)