# Sharp
A json (framework) alternative to make it easier programming in a .json file, it also has benefits some features that json files does not have. <br>

## Getting started
To get started, you can use Piargs or git clone to get it. (your choise) After you've installed/downloaded Sharp, you can use two types of it, compiled or direct. Compiled it default <br>

**Diffrence**
  Direct: will let you directly run scripts in the file, like in json files
  Compile: will compile the .shrp files into a .json file
to use direct, you can use ```type: "direct"```.

## Programming in it
here are all the current keywords: ```type, variables, scripts```, and comments are /* */ and // .

variables:
 To use variables, use:
    variables: { 
        hello = world, 
        num = 69
    }

scripts:
 To use variables, use:
    scripts: { 
      hello: echo hello world, /* or */
      saynum: echo $num
    }
