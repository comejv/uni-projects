# Makefile Documentation

## Introduction

This Makefile is designed for a C project that includes support for generating documentation, running system tests, and compiling with various debugging and testing options.

## Targets

- `all`: Compiles the project.
- `clean`: Removes all generated files.
- `doc`: Generates documentation using Doxygen.
- `systests`: Runs system tests.
- `showGcov`: Shows code coverage information.

## Variables

- `CC`: The C compiler to use.
- `CFLAGS`: Flags for the C compiler.
- `CPPFLAGS`: Flags for the C preprocessor.
- `SRCDIR`: Directory containing source files.
- `OBJDIR`: Directory for object files.
- `EXECDIR`: Directory for the executable.
- `HEADERSDIR`: Directory containing header files.
- `DOCDIR`: Directory for documentation.
- `DOCCONF`: Doxygen configuration file.
- `SRCS`: All source files.
- `HEADERS`: All header files.
- `OBJS`: All object files.
- `MAIN_OBJ`: The main object file.
- `EXEC`: The executable file.
- `LDFLAGS`: Flags for the linker.
- `DEBUG`: Debugging level.
- `ASAN`: AddressSanitizer flags.
- `TESTS`: Testing flags.

## Usage

To compile the project, run:
```bash
make all
```

To run system tests, run:
```bash
make systests
```
To show code coverage of the tests run use :
```bash
make showGcov
```

