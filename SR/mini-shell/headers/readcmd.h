/**
 * @file readcmd.h
 * @brief Defines functions and structures related to reading a command from an input stream.
 */

#ifndef __READCMD_H
#define __READCMD_H

#include <stdio.h>
#include <stddef.h>
#include <stdlib.h>
#include <errno.h>
#include <limits.h>
#include <string.h>

/**
 * @brief Reads a command line from an input stream.
 *
 * This function reads a command line from the standard input stream. It parses the command
 * line and allocates memory for a `cmdline` structure containing the parsed information.
 *
 * @return A pointer to a newly allocated `cmdline` structure, or `nullptr` if an error
 *         occurs (e.g., memory allocation failure) or the input stream is closed.
 *
 * @note If an error occurs during memory allocation, an error message is printed to
 *       standard error and the program exits.
 */
struct cmdline *readcmd(void);

/**
 * @brief Structure representing a parsed command line.
 *
 * This structure stores the information extracted from a command line parsed by the
 * `readcmd` function.
 */
struct cmdline {
    /**
     * @brief Error message, if not null.
     *
     * If this field is not null, it contains an error message that should be displayed.
     * In this case, all other fields of the structure are null.
     */
    char *err;

    /**
     * @brief Name of the file for input redirection, if not null.
     *
     * If this field is not null, it specifies the name of the file to use for input
     * redirection for the command.
     */
    char *in;

    /**
     * @brief Name of the file for output redirection, if not null.
     *
     * If this field is not null, it specifies the name of the file to use for output
     * redirection for the command.
     */
    char *out;

    /**
     * @brief Sequence of commands, if not null.
     *
     * This field points to an array of commands. Each command is represented by an
     * array of strings, where the last string is a null pointer. The null pointer at
     * the end of the array of commands marks the end of the sequence.
     *
     * See the detailed explanation below for the structure of the `seq` field.
     */
    char ***seq;

    /**
     * @brief Background flag (1 = background command, 0 otherwise).
     *
     * This flag indicates whether the command should be run in the background.
     */
    int bg;
};

/**
 * @brief Structure description of the `seq` field in `cmdline`.
 *
 * A command line can be a sequence of commands, where the output of each command
 * is piped to the input of the next one. This structure describes the data format
 * used to represent such a sequence.
 *
 * - A **command** is represented by an array of strings (`char **`). The last
 *   string in the array is always a null pointer.
 * - A **sequence** is represented by an array of commands (`char ***`). The last
 *   command in the sequence is always represented by a null pointer.
 *
 * When a `cmdline` structure is returned by `readcmd()`, the `seq[0]` pointer is
 * never null.
 */

#endif // __READCMD_H
