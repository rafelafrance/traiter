%{

#include "lexer.h"

%}

%%

([[:digit:]]{1,3}(,[[:digit:]]{3}){1,3}|[[:digit:]]+)(\.[[:digit:]]+)? {
  return NUMBER;
}

[[:alpha:]][[:alnum:]]+   { return WORD; }

\s+     { return SPACES; }

"("     { return LPAR; }
")"     { return RPAR; }
"["     { return LSQB; }
"]"     { return RSQB; }
":"     { return COLON; }
","     { return COMMA; }
";"     { return SEMI; }
"+"     { return PLUS; }
"-"     { return DASH; }
"*"     { return STAR; }
"/"     { return SLASH; }
"|"     { return VBAR; }
"&"     { return AMPER; }
"<"     { return LESS; }
">"     { return GREATER; }
"="     { return EQUAL; }
"%%"    { return PERCENT; }
"{"     { return LBRACE; }
"}"     { return RBRACE; }
"@"     { return AT; }
"."     { return DOT; }
"?"     { return QUEST; }
"\\"    { return BSLASH; }

.       { return OTHER; }

%%


int yywrap(void) {
  return 1;
}
