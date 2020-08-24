from grammar import SoLangVisitor, SoLangParser
import llvmlite.ir as ir
import llvmlite.binding as llvm


class MyVisitor(SoLangVisitor):
    def visitProg(self, ctx: SoLangParser.ProgContext):
        # llvm init
        llvm.initialize()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()

        # define types
        self.i64 = ir.IntType(64)
        self.f64 = ir.FloatType()

        # int64_t main()
        ftype_main = ir.FunctionType(self.i64, [])
        module = ir.Module(name='sokoide_module')
        fn_main = ir.Function(module, ftype_main, name="main")
        block = fn_main.append_basic_block(name='entrypoint')

        # function prototype (external linkage implemented in builtin.c) for
        # void write(int64_t)
        ftype_write = ir.FunctionType(ir.VoidType(), [self.f64])
        self.fn_write = ir.Function(module, ftype_write, name="write")

        # make a block for main (entrypoint)
        self.builder = ir.IRBuilder(block)

        # visit
        # print("* visitProg. {}".format(ctx))
        ret = self.visitChildren(ctx)

        # return 0
        self.builder.ret(ir.Constant(self.i64, 0))

        llvm_ir = str(module)
        llvm_ir_parsed = llvm.parse_assembly(llvm_ir)
        with open("build/out.ll", "w") as f:
            f.write(str(llvm_ir_parsed))

        # ret is always None
        return ret

    def visitLine(self, ctx: SoLangParser.LineContext):
        # print("* visitLine. {}".format(ctx))
        lno = 1
        for expr in ctx.children:
            ret = self.visit(expr)
            # call write()
            self.builder.call(self.fn_write, (ret,), name="write")
            lno += 1
        # return only the last expr
        return ret

    def visitParExpr(self, ctx: SoLangParser.ParExprContext):
        # print("* visitParExpr. {}".format(ctx.getText()))
        ret = self.visit(ctx.children[1])
        return ret

    def visitIntExpr(self, ctx: SoLangParser.IntExprContext):
        # print("* visitIntExpr. {}, {}".format(ctx.getText(), ctx.INT()))
        # return int(ctx.INT().getText())
        return ir.Constant(self.f64, float(ctx.INT().getText()))

    def visitMulDivExpr(self, ctx: SoLangParser.MulDivExprContext):
        # print("* mulDiv")
        lhs = self.visit(ctx.children[0])
        rhs = self.visit(ctx.children[2])
        if ctx.children[1].getText() == '*':
            ret = self.builder.fmul(lhs, rhs, name='mul_tmp')
        else:
            ret = self.builder.fdiv(lhs, rhs, name='div_tmp')
        return ret

    def visitAddSubExpr(self, ctx: SoLangParser.AddSubExprContext):
        # print("* addSub")
        lhs = self.visit(ctx.children[0])
        rhs = self.visit(ctx.children[2])
        if ctx.children[1].getText() == '+':
            ret = self.builder.fadd(lhs, rhs, name='add_tmp')
        else:
            ret = self.builder.fsub(lhs, rhs, name='sub_tmp')
        return ret
