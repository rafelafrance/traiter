#include <stdio.h>
#include "lexer.h"

extern int yylex();
extern int yylineno;
extern char* yytext;

char* names[] = {
  NULL,
  "spaces",
  "number",
  "word",
};

int main(void) {
  int ntoken, vtoken;

  ntoken = yylex();
  while(ntoken) {
    printf("%d\t%s\n", ntoken, yytext);
    ntoken = yylex();
  }

  return 0;
}
