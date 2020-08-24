ANTLR4=java -jar /usr/local/lib/antlr-4.8-complete.jar

GRAMMAR_PY=build/grammar/SoLangLexer.py \
build/grammar/SoLang.interp \
build/grammar/SoLang.tokens \
build/grammar/SoLangLexer.interp \
build/grammar/SoLangLexer.tokens \
build/grammar/SoLangParser.py

all: $(GRAMMAR_PY) build/builtin.ll

run: all
	python main.py

clean:
	[ -d build ] && rm -rf build/*
	[ -d __pycache__ ] && rm -rf __pycache__

test: all
	echo "1+3*7" | python main.py
	echo "3*(3+5)/4\n1+2*3" | python main.py

# generation rules
$(GRAMMAR_PY): grammar/SoLang.g4
	[ -d build ] || mkdir build
	$(ANTLR4) grammar/SoLang.g4 -no-listener -visitor -o build

build/builtin.ll: builtin.c
	[ -d build ] || mkdir build
	clang -emit-llvm -S -O -o build/builtin.ll builtin.c

