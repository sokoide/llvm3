// Please generate listener by
//
// Mac/Linux: alias antlr4=java -jar /path/to/antlr-4.8-complete.jar $*)
// Win: antlr4.bat contains 'java -jar c:\tools\antlr-4.8-complete.jar %*'
// Then run,
// antlr4 SoLang.g4 -no-listener -visitor -o generated

grammar SoLang;

options {
	language = Python3;
}

prog:    (line NEWLINE)* ;

line:    expr* ;

expr:    expr ('*'|'/') expr #MulDivExpr

    |    expr ('+'|'-') expr #addSubExpr
    |    INT #intExpr
    |    '(' expr ')' #parExpr
    ;

NEWLINE : [\r\n]+ ;

INT     : [0-9]+ ;

