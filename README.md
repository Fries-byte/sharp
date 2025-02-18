# Sharp
A json (framework) alternative to make it easier programming in a .json file, it also has benefits some features that json files does not have. <br>

## Getting started
To get started, you can use Piargs or git clone to get it. (your choise) After you've installed/downloaded Sharp, you can use two types of it, compiled or direct. Compiled it default <br>

**Diffrence**
  Direct: will let you directly run scripts in the file, like in json files <br>
  Compile: will compile the .shrp files into a .json file <br>
to use direct, you can use ```type: "direct"```. <br>

## Programming in it
here are all the current keywords: ```type, variables, scripts```, and comments are /* */ and // . <br>

variables: <br>
 To use variables, use: <br>
    variables: {  <br>
        hello = world,  <br>
        num = 69 <br>
    }

scripts: <br>
 To use variables, use: <br>
    scripts: { <br>
      hello: echo hello world, /* or */ <br>
      saynum: echo $num <br>
    } <br>
