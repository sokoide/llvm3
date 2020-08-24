# LLVM3

## About

* LLVM frontend (IR generation) Simple Calculator example with Antlr4 for Python3
* Please refer to the following 2 for simpler versions
** [LLVM1](https://github.com/sokoide/llvm1)
** [LLVM2](https://github.com/sokoide/llvm2)


## How to build

* Change ANTLR4 in Makefile and run `make` to build

## How to run

* Run `make test` to see what happens
* It compiles `1+3*7` into IR and run it by lli (interpreter)
* Then it compiles `3*(3+5)/4 <LF> 1+2*` into another IR, makes a native binary `linked` and runs it

```sh
make test

echo "* running main.py for 1+3*7"
* running main.py for 1+3*7
echo "1+3*7" | python main.py
llvm-link build/out.ll build/builtin.ll -S -o build/linked.ll
warning: Linking two modules of different target triples: build/builtin.ll' is 'x86_64-apple-macosx10.15.0' whereas 'llvm-link' is 'unknown-unknown-unknown'

echo "* running linked.ll by lli (inetrpreter)"
* running linked.ll by lli (inetrpreter)
lli build/linked.ll
22.000000
echo "* running another test for 3*(3+5)/4 <LF> 1+2*3"
* running another test for 3*(3+5)/4 <LF> 1+2*3
echo "3*(3+5)/4\n1+2*3" | python main.py
llvm-link build/out.ll build/builtin.ll -S -o build/linked.ll
warning: Linking two modules of different target triples: build/builtin.ll' is 'x86_64-apple-macosx10.15.0' whereas 'llvm-link' is 'unknown-unknown-unknown'

llc build/linked.ll -o build/linked.s
clang build/linked.s -o build/linked
echo "* running native linked"
* running native linked
build/linked
6.000000
7.000000
```

* The generated IR for the 2nd test is as below

```sh
$ cat build/linked.ll
; ModuleID = 'llvm-link'
source_filename = "llvm-link"
target datalayout = "e-m:o-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-apple-macosx10.15.0"

@.str = private unnamed_addr constant [5 x i8] c"%lf\0A\00", align 1

define i64 @main() {
entrypoint:
  %add_tmp = fadd float 3.000000e+00, 5.000000e+00
  %mul_tmp = fmul float 3.000000e+00, %add_tmp
  %div_tmp = fdiv float %mul_tmp, 4.000000e+00
  call void bitcast (i64 (float)* @write to void (float)*)(float %div_tmp)
  %mul_tmp.1 = fmul float 2.000000e+00, 3.000000e+00
  %add_tmp.1 = fadd float 1.000000e+00, %mul_tmp.1
  call void bitcast (i64 (float)* @write to void (float)*)(float %add_tmp.1)
  ret i64 0
}

; Function Attrs: nofree nounwind ssp uwtable
define i64 @write(float %0) #0 {
  %2 = fpext float %0 to double
  %3 = tail call i32 (i8*, ...) @printf(i8* nonnull dereferenceable(1) getelementptr inbounds ([5 x i8], [5 x i8]* @.str, i64 0, i64 0), double %2)
  %4 = sext i32 %3 to i64
  ret i64 %4
}

; Function Attrs: nofree nounwind
declare i32 @printf(i8* nocapture readonly, ...) local_unnamed_addr #1

attributes #0 = { nofree nounwind ssp uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "frame-pointer"="all" "less-precise-fpmad"="false" "min-legal-vector-width"="0" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="penryn" "target-features"="+cx16,+cx8,+fxsr,+mmx,+sahf,+sse,+sse2,+sse3,+sse4.1,+ssse3,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { nofree nounwind "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "frame-pointer"="all" "less-precise-fpmad"="false" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="penryn" "target-features"="+cx16,+cx8,+fxsr,+mmx,+sahf,+sse,+sse2,+sse3,+sse4.1,+ssse3,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }

!llvm.ident = !{!0}
!llvm.module.flags = !{!1, !2}

!0 = !{!"clang version 10.0.1 "}
!1 = !{i32 1, !"wchar_size", i32 4}
!2 = !{i32 7, !"PIC Level", i32 2}
```
