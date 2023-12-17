from lark import Lark

class TLDBParser:
  @staticmethod
  def parser(grammar: str, start: str = "query"):
    return Lark(grammar = grammar, start = start, parser = "lalr")