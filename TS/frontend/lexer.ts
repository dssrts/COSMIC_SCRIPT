//parang set sa python
export enum TokenType {

    //literals
    Null = "Null",
    Number = "Number",
    Identifier = "Identifier",

    //operators
    Equals = "Equals",
    OpenParen = "OpenParen",
    CloseParen = "CloseParen",
    BinaryOperator = "BinaryOperator",

    //reserved words
    Let = "Let",
    //Outer = "Outer", 

    //end of file
    EOF = "EOF"
}
// this is a dictionary that holds the reserved words
const KEYWORDS: Record<string, TokenType> = {
    "let": TokenType.Let,
    "null": TokenType.Null,
    // "outer": TokenType.Outer,

}

//eto na yung tokens
//interface is parang class sa python
export interface Token {
    value: string,
    type: TokenType,
}

// this returns a token
function token (value = '', type: TokenType): Token{
    return { value, type };
}


//checks if the input is an alphabet
function isalpha(src: string){
    return src.toUpperCase() != src.toLowerCase();
}

//checks if the input is an int
function isint(str: string){
    const c = str.charCodeAt(0);
    const bounds = ['0'.charCodeAt(0), '9'.charCodeAt(0)];
    return (c >= bounds[0] && c <= bounds[1]);
}


function isskippable(str: string){
    return str == ' ' || str == "\n" || str == "\t";
}

export function tokenize (sourceCode: string): Token[]{
    const tokens = new Array<Token>();
    const src = sourceCode.split("");

    while(src.length > 0){
    //remember .shift() returns a value from an array then deletes it after
        if(src[0] == "("){
            tokens.push(token(src.shift(), TokenType.OpenParen))
        } else if(src[0] == ")"){
            tokens.push(token(src.shift(), TokenType.CloseParen))
        } else if (src[0] == "+" || src[0] == "-" || src[0] == "*" || src[0] == "/" || src[0] == "%"){
            tokens.push(token(src.shift(), TokenType.BinaryOperator))
        } else if (src[0] == '='){
            tokens.push(token(src.shift(), TokenType.Equals))
        } else{
            //handle multicharacter tokens
            // cat
            // outer
            //build number token
            if (isint(src[0])){
                let num = ""; //string to hold the number
                //remember yung shift tinatanggal yung current character then returns it
                //so laging nasa index 0 yung current
                
                //while there's a character in src (array) and the next character is an int
                while (src.length > 0 && isint(src[0])){
                    num += src.shift();
                }
                //push the number string to tokens array
                tokens.push(token(num, TokenType.Number));
                
                //same thing with is alpha
            } else if (isalpha(src[0])){
                let ident = ""; // store dito yung word
                while (src.length > 0 && isalpha(src[0])){
                    ident += src.shift();
                }
                //check for reserved keywords
                const reserved = KEYWORDS[ident];
                
                //if the dictionary KEYWORDS didnt return anything
                if (typeof reserved == "string"){
                    //if there's a value in KEYWORDS, return reserved
                    tokens.push(token(ident, reserved));
                    
                } else {
                    tokens.push(token(ident, TokenType.Identifier));
                }
            // if it's a whitespace
            } else if (isskippable(src[0])){
                src.shift();
            } else {
                console.log("Unrecognized character: ", src[0])
                Deno.exit(1);
            }
        }
    }
    tokens.push({type: TokenType.EOF, value:"End"});
    return tokens;
}

/*
const source = await Deno.readTextFile("./test.txt")
for(const token of tokenize(source)){
    console.log(token);
}*/