from grammar import SoLangVisitor, SoLangParser


class MyVisitor(SoLangVisitor):
    def visitProg(self, ctx: SoLangParser.ProgContext):
        print("* visitProg. {}".format(ctx))
        ret = self.visitChildren(ctx)
        print("* visitProg leave={}".format(ret))
        # ret is always None
        return ret

    def visitLine(self, ctx: SoLangParser.LineContext):
        print("* visitLine. {}".format(ctx))
        lno = 1
        for expr in ctx.children:
            ret = self.visit(expr)
            print("line {}: ret={}".format(lno, ret))
            lno += 1
        # return only the last expr
        return ret

    def visitParExpr(self, ctx: SoLangParser.ParExprContext):
        print("* visitParExpr. {}".format(ctx.getText()))
        ret = self.visit(ctx.children[1])
        print("* visitPar leave={}".format(ret))
        return ret

    def visitIntExpr(self, ctx: SoLangParser.IntExprContext):
        print("* visitIntExpr. {}, {}".format(ctx.getText(), ctx.INT()))
        # return self.visitChildren(ctx)
        return int(ctx.INT().getText())

    def visitMulDivExpr(self, ctx: SoLangParser.MulDivExprContext):
        print("* mulDiv")
        retl = self.visit(ctx.children[0])
        retr = self.visit(ctx.children[2])
        print("* visitMulDivExpr. {}, {} {}".format(ctx.getText(),
                                                    ctx.expr(0), ctx.expr(1)))
        if ctx.children[1].getText() == '*':
            ret = retl * retr
        else:
            ret = retl / retr
        print("* visitMulDivExpr leave={}".format(ret))
        return ret

    def visitAddSubExpr(self, ctx: SoLangParser.AddSubExprContext):
        print("* addSub")
        retl = self.visit(ctx.children[0])
        retr = self.visit(ctx.children[2])
        print("* visitAddSubExpr. {}, {} {}".format(ctx.getText(),
                                                    ctx.expr(0), ctx.expr(1)))
        if ctx.children[1].getText() == '+':
            ret = retl + retr
        else:
            ret = retl - retr
        print("* visitAddSubExpr leave={}".format(ret))
        return ret
