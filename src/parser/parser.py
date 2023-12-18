from lark import Lark

class TLDBParser:
  @staticmethod
  def parser(grammar: str):
    return Lark(grammar = grammar, start = "query", parser = "lalr")