<p align="center">
<img src="https://img.shields.io/github/languages/count/comejv/uni-projects" alt="GitHub language count">
<img src="https://img.shields.io/github/languages/top/comejv/uni-projects" alt="GitHub top language">
<img src="https://img.shields.io/github/repo-size/comejv/uni-projects" alt="GitHub repo size">
<img src ="https://img.shields.io/github/last-commit/comejv/uni-projects" alt="GitHub last commit">
</p>

# University Projects

> **Note**: Most projects were completed in pairs with [Euxem](https://github.com/euxem).

To clone a part of this repository, use my [sparse-clone](https://github.com/comejv/utils-and-games/tree/main/git-sparse-clone) script.

Info: some projects are stored in a separate repository:

<p align="center" href="https://github.com/comejv/utils-and-games">
<img src="https://github-link-card.s3.ap-northeast-1.amazonaws.com/comejv/utils-and-games.png" width="460px">
</p>

Or in their own repository, accessible via a link further down this page.

***

## Repository Stats

```
-------------------------------------------------------------------------------
Language                     files          blank        comment           code
-------------------------------------------------------------------------------
C                               72            599            979          11253
Python                          13            190            317           2079
C/C++ Header                    20            212            210            471
SQL                              4              8             21            202
make                             3             59             15             89
Markdown                         3             49              0            116
Java                            70            753           2587          13435
-------------------------------------------------------------------------------
SUM:                           185           1870           4129          27529
-------------------------------------------------------------------------------
```

***

## INF101 [![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff)](#)

> Computer methods and programming techniques

[**Blackjack**](https://github.com/comejv/utils-and-games/tree/main/blackjack): a CLI blackjack game with bots and game options.

***

## INF201 [![OCaml](https://img.shields.io/badge/OCaml-EC6813?logo=ocaml&logoColor=fff)](#)

> Algorithms and functional programming

[**Checkers**](https://github.com/comejv/utils-and-games/tree/main/dames): a simple checkers game on a hexagonal board in CLI.

***

## INF203 [![C](https://img.shields.io/badge/C-00599C?logo=c&logoColor=white)](#)

> System and programming environment

[**Cow**](https://github.com/comejv/utils-and-games/tree/main/cow): A program based on the cowsay CLI application. It allows you to display a cow with a custom message and has some options and games.

***

## INF301 [![C](https://img.shields.io/badge/C-00599C?logo=c&logoColor=white)](#)

> Algorithms and imperative programming

- [**APP2 - Curiosity**](INF301/APP2/): instruction interpreter for a robot that moves in a 2D terrain (testing and terrain generation in [INF304](INF304))
- [**APP3 - Phylogenetic Tree**](INF301/APP3/): creation, reading, and manipulation of phylogenetic trees

***

## INF304 [![C](https://img.shields.io/badge/C-00599C?logo=c&logoColor=white)](#)

> Basics of software development: modularization, testing

[**INF304**](INF304/) follows [INF301/APP2](INF301/APP2/) by addressing terrain generation and interpreter testing.

***

## INF402 [![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff)](#) [![C](https://img.shields.io/badge/C-00599C?logo=c&logoColor=white)](#)

> Introduction to logic

[**INF402 - Project**](INF402/): a program that solves part of the "Hashiwokakero" game (or "Bridges" for short) using computer vision to understand the board and logic to solve the problem. Implementation of a simple WalkingSAT.

***

## INF403 [![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff)](#) ![](https://img.shields.io/badge/sql-yellow)

> Relational data management and applications

[**INF403 - Project**](INF403/): database management application for a company producing and selling liquid hydrogen.

## INF404 [![C](https://img.shields.io/badge/C-00599C?logo=c&logoColor=white)](#)

> Software project

[**INF404 - Project**](https://github.com/euxem/Projet_shrek): interpreter for a language we created, which aims to add a functional programming paradigm to the graphical language dot, which is only declarative. Stored in my partner's repository, [Euxem](https://github.com/euxem).

## PROG5 [![C](https://img.shields.io/badge/C-00599C?logo=c&logoColor=white)](#)

> Software project

[**ARM-SIMULATOR**](https://github.com/comejv/ARM-SIM): this project aims to develop a simulator for a subset of the ARMv5 instruction set. The simulator is designed to execute machine code written for the ARMv5 instruction set on a host machine with a different instruction set. Although the main target host architecture is Intel x86 (32-bit) or x86-64 (64-bit), the simulator code is written in a portable manner and can be compiled and run on other architectures. Project completed in a team of 6 people.

## Systems and Networks [![C](https://img.shields.io/badge/C-00599C?logo=c&logoColor=white)](#)

> Semester projects

[**MINI-SHELL**](SR/mini-shell): creation of a shell capable of managing program execution and internal commands, putting tasks in the background and bringing them to the foreground or suspending them.

[**FTP**](https://github.com/Luminosaa/FTP): FTP server and client capable of handling multiple connections, with load balancing between multiple servers using a master-slave architecture.

## PROG6 [![Java](https://img.shields.io/badge/Java-%23ED8B00.svg?logo=openjdk&logoColor=white)](#)

[**KUBE**](https://github.com/comejv/kube): Java implementation of a board game with a Swing graphical interface, artificial intelligence to compete against the computer, and network integration for online play.

## MOCA [![OCaml](https://img.shields.io/badge/OCaml-EC6813?logo=ocaml&logoColor=fff)](#)

> Semester project

[**Project**](https://github.com/comejv/MOCA): Project for refactoring and improving an existing code base. The goal was to apply good development practices and use various tools to improve code quality, security, and performance. Among the improvements made: project modularization, creation of makefiles, implementation of unit tests with CUTest, correction of memory leaks with Valgrind and ASAN, performance optimization with gprof, and addition of documentation with Doxygen. The project also integrated advanced techniques such as the use of static and dynamic libraries, code coverage with gcov, and dynamic analysis with AFL.

## Compilation

> Semester project

[**Project**](https://github.com/quezii/MiniJava/): Implementation of a compiler for a subset of Java (Mini Java) that generates x86-64 assembly code. The compiler supports object-oriented programming (classes, inheritance, method dispatch), control structures (if, for, return), primitive types (integers, booleans, null), string operations, method calls, and expressions. The project is structured in several modules handling the different compilation phases: AST, lexer/parser, type checking, and code generation. The compiler ensures correct memory management with object allocation on the heap and construction of vtables for dynamic method dispatch.
