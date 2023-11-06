// deno-lint-ignore-file no-empty-interface
export type NodeType = 
| "Program" 
| "NumericLiteral" 
| "NullLiteral"
| "Identifier" 
| "BinaryExpr" 
| "CallExpr" 
| "UnaryExpr" 
| "FunctionDeclaration";


//class statement
export interface Stmt {
    kind: NodeType;
}

//class program that has a kind but has a body
export interface Program extends Stmt{
    kind: "Program";
    body: Stmt[];
}

//class expression that has a kind
export interface Expr extends Stmt {}

//class binary expression that has a kind but also has a left and right and operator
export interface BinaryExpr extends Expr{
    kind: "BinaryExpr"
    left: Expr;
    right: Expr;
    operator: string;
}

//has a kind and has a symbol
export interface Identifier extends Expr{
    kind: "Identifier";
    symbol: string;
}

//has a kind and has a value
export interface NumericLiteral extends Expr{
    kind: "NumericLiteral";
    value: number;
}

export interface NullLiteral extends Expr{
    kind: "NullLiteral";
    value: "null";
}


