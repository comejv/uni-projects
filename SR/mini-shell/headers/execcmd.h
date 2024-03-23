/**
 * @file execcmd.h
 * @brief Defines functions related to executing parsed commands.
 */

#ifndef __EXECCMD_H
#define __EXECCMD_H

#include "csapp.h"
#include "global.h"
#include "macro.h"
#include "readcmd.h"
#include <grp.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>

/**
 * @def MAXPATHLEN
 * @brief Defines the maximum allowed length for a pathname.
 *
 * This macro defines the maximum number of characters allowed in a pathname
 * on the system. It has a value of 100, which is a common maximum length
 * across different operating systems. However, it is important to note that
 * the actual maximum pathname length may vary depending on the specific
 * system configuration.
 */
#define MAXPATHLEN 100

/**
 * @brief Executes a parsed command.
 *
 * This function takes a pointer to a `cmdline` structure and executes the
 * corresponding command. It handles aspects like creating child processes,
 * managing pipes, and performing input/output redirections.
 *
 * @param l Pointer to a `cmdline` structure representing the command to
 * execute.
 *
 * @note This function does not return any value.
 */
void execution(struct cmdline *l);

/**
 * @brief Frees the memory allocated for pipes.
 *
 * This function takes an array of pipe descriptor arrays (`pipes`) and the
 * total number of commands (`n_cmd`). It frees the memory allocated for each
 * pipe descriptor pair within the provided `pipes` array.
 *
 * @param pipes Array of pipe descriptor arrays, where each array represents the
 *              pipes for a specific command.
 * @param n_cmd The total number of commands in the pipeline.
 *
 * @note This function does not return any value.
 */
void free_pipes(int **pipes, int n_cmd);

/**
 * @brief Closes unnecessary pipes for a specific command.
 *
 * This function closes all pipe descriptors except those needed for the
 * command at the specified index (`rang_cmd`) within a sequence of commands
 * (`n_cmd`). It takes into account the overall pipeline structure (`pipes`)
 * to determine which pipes to close.
 *
 * @param rang_cmd The index of the command for which to close unnecessary
 * pipes.
 * @param n_cmd The total number of commands in the pipeline.
 * @param pipes Array of pipe descriptor arrays, where each array represents the
 *              pipes for a specific command.
 *
 * @note This function does not return any value.
 */
void connection_pipes(int rang_cmd, int n_cmd, int **pipes);

/**
 * @brief Creates pipe descriptors for a sequence of commands.
 *
 * This function allocates memory and creates pipe descriptors for all commands
 * in a sequence (`n_cmd`). It returns an array of pipe descriptor arrays, where
 * each array represents the pipes for a specific command.
 *
 * @param n_cmd The total number of commands in the pipeline.
 *
 * @return An array of pipe descriptor arrays, or `NULL` on error.
 */
int **create_pipes(int n_cmd);

/**
 * @brief Counts the number of commands in a sequence.
 *
 * This function takes an array of command arrays (`seq`) and returns the number
 * of individual commands within that sequence.
 *
 * @param seq An array of arrays of strings, where each inner array represents a
 *            command (the last string in each inner array is a null pointer).
 *
 * @return The number of commands in the provided sequence.
 */
int compte_cmd(char ***seq);

/**
 * @brief Connects input and output for a specific command within a sequence.
 *
 * This function performs input and output redirection based on the provided
 * `cmdline` structure, the total number of commands (`n_cmd`), and the rank of
 * the current command being processed by a child process
 * (`current_commande_rank`).
 *
 * @param l Pointer to a `cmdline` structure representing the command.
 * @param n_cmd The total number of commands in the pipeline.
 * @param current_commande_rank The rank of the current command being processed
 * by the child process.
 *
 * @note This function does not return any value.
 */
void connect_in_out(struct cmdline *l, int n_cmd, int current_commande_rank);

/**
 * @brief Handles internal commands like "cd", "bg", "fg", etc.
 *
 * This function checks if the given command (cmd) is an internal command
 * and executes it if so.
 *
 * @param cmd An array of strings representing the command (first string is
 * the command name, last string is a null pointer).
 *
 * @return 1 if the command was internal and handled, 0 otherwise.
 */
int internal_cmd(char **cmd);

#endif // __EXECCMD_H
