// #1
function funcOne() {
    let a = 5;
    if(a > 1) {
        a = 3;
    }
    alert(`inside the funcOne function ${a}`);
}

// #1.1 - run in the console:
// a=3, becuase the variable a is declared with let
funcOne()
// #1.2 What will happen if the variable is declared
// with const instead of let ?
// an error will be thrown because we are trying to reassign a constant variable

//#2
//let a = 0;
function funcTwo() {
    a = 5;
}

function funcThree() {
    alert(`inside the funcThree function ${a}`);
}

// #2.1 - run in the console:
// a=5, because funcTwo is called before funcThree
funcThree()
funcTwo()
funcThree()
// #2.2 What will happen if the variable is declared
// with const instead of let ?
// an error will be thrown because we are trying to reassign a constant variable


//#3
function funcFour() {
    window.a = "hello";
}


function funcFive() {
    alert(`inside the funcFive function ${a}`);
}

// #3.1 - run in the console:
//inside the funcFive function hello, because funcFour is called before funcFive
funcFour()
funcFive()

//#4
//let a = 1;
function funcSix() {
    let a = "test";
    alert(`inside the funcSix function ${a}`);
}


// #4.1 - run in the console:
// inside the funcSix function test, because the variable a inside funcSix is a different variable from the global a
funcSix()
// #4.2 What will happen if the variable is declared
// with const instead of let ?
// no difference, it will still alert "test" because the variable a inside funcSix is a different variable from the
global

//#5
let a = 2;
if (true) {
    let a = 5;
    alert(`in the if block ${a}`);
}
alert(`outside of the if block ${a}`);

// #5.1 - run the code in the console
// in the if block 5
// #5.2 What will happen if the variable is declared
// with const instead of let ?
// no difference, it will still alert 5 because the variable a inside the if block is a different variable from the global a