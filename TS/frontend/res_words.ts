/*
function isalpha(src: string){
    return src.toUpperCase() != src.toLowerCase();
}*/

function res_word(input:string): string{
//check if it's an alphabet

    const input_arr = input.split("");
    const msg = "A";
    const msg2 = "not A";
    if (input_arr[0]== "a"){
        return msg;
    }
    else{
        return msg2;
    }
}
// set an array of res words


const word = prompt("input a word: ") as string;

console.log(res_word(word));