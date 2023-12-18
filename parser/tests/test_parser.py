from pathlib import Path

from ..tldb_parser import TLDBParser
from ..tldb_transformer import TLDBParserTransformer

with open(Path(__file__).parent / "../tldb.grammar.lark", "r") as f:
  grammar = f.read()

parser = TLDBParser.parser(grammar)
transformer = TLDBParserTransformer()

def test_insert_op_integer():
  stdin = "insert 0x000 0x000 1"
  expected = "insert|0x000|0x000|1.0"

  tree = parser.parse(stdin)
  _, transformed = transformer.transform(tree)

  # parse-out the timestamp part
  output = "|".join(transformed.split("|")[0:-1])
  assert output == expected

def test_insert_op_float():
  stdin = "insert 0x000 0x000 1.2"
  expected = "insert|0x000|0x000|1.2"

  tree = parser.parse(stdin)
  _, transformed = transformer.transform(tree)
  
  # parse-out the timestamp part
  output = "|".join(transformed.split("|")[0:-1])
  assert output == expected
