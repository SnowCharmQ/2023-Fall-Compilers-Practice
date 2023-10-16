%{
    #define YYSTYPE char *
    #include "lex.yy.c"
    int yyerror(char* s);
    int check_ipv4(char* s);
    int check_ipv6(char* s);
%}

%token X
%token DOT
%token COLON

%%

IP: IPv4 { printf("IPv4\n"); }
    | IPv6 { printf("IPv6\n"); }
    ;

IPv4: X DOT X DOT X DOT X { 
    if (!check_ipv4($1) || !check_ipv4($3) || !check_ipv4($5) || !check_ipv4($7)) {
        yyerror("Invalid\n");
        return 0;
    }
    int a1 = atoi($1);
    int a2 = atoi($3);
    int a3 = atoi($5);
    int a4 = atoi($7);
    if (a1 < 0 || a1 > 255 || a2 < 0 || a2 > 255 || a3 < 0 || a3 > 255 || a4 < 0 || a4 > 255) {
        yyerror("Invalid\n");
        return 0;
    }
}

IPv6: X COLON X COLON X COLON X COLON X COLON X COLON X COLON X { 
    int flag = check_ipv6($1) * check_ipv6($3) * check_ipv6($5) * check_ipv6($7) * 
                check_ipv6($9) * check_ipv6($11) * check_ipv6($13) * check_ipv6($15);
    if (!flag) {
        yyerror("Invalid\n");
        return 0;
    }
}

%%

int yyerror(char* s) {
    fprintf(stderr, "%s\n", "Invalid");
    return 1;
}

int check_ipv4(char* s) {
    if (strlen(s) == 1) {
        return 1;
    } else {
        return s[0] != '0';
    }
}

int check_ipv6(char* s) {
    return strlen(s) > 0 && strlen(s) <= 4;
}

int main() {
    yyparse();
}
