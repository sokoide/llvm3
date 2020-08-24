import grammar
import antlr4
import sys


def main():
    print("* 'prog' started")
    input = ''.join(sys.stdin.readlines())
    print("* parsing '{}'".format(input))
    lexer = grammar.SoLangLexer(antlr4.InputStream(input))

    token_stream = antlr4.CommonTokenStream(lexer)
    parser = grammar.SoLangParser(token_stream)

    visitor = grammar.MyVisitor()
    ret = visitor.visitProg(parser.prog())
    print("* 'prog' ended with {}".format(ret))


if __name__ == '__main__':
    main()
