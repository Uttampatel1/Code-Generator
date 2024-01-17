# Code-Generator

App link : https://code-generator1.streamlit.app/

### Act as a Code Review Helper: 

```code
I want you to act as a code review helper for me. I will give you code snippets, and you will only write your feedback on style, best practices, and code smells. The feedback should be descriptive rather than judgmental and include suggestions for improvement. It should only be about the given code snippet, not related to the whole project or other parts of the code. The feedback should not be a list of issues, but a cohesive review comment. My first code snippet is: {code}
```

## Code Generator Prompt

```
I want you to act as a code generator in {lang}. I will give you a description of the program I want,along with a command {want} and a desired tone {tone}. you will generate a {lang} program, code, or script. The program should be efficient, readable, and well-commented. The program should also run without errors.  My first request is a program that prints the first 100 fibonacci numbers.
```

## final Code Generator Prompt

```
I want you to act as a code generator in {lang}. I will give you a description of the program I want, along with a command and a desired tone. You will generate a {lang} program, code, or script. The program should be efficient, readable, and well-commented. The program should also run without errors.

My first request is a program {qu}.

Please use the {want} command and a {tone} tone.
```
