#ifndef __HANDLERS_H
#define __HANDLERS_H

#include "csapp.h"
#include "global.h"
#include "linked_list.h"
#include <signal.h>
#include <sys/wait.h>

/**
 * @file handlers.h
 * @brief This header file contains the function prototypes for signal handling.
 *
 * The functions declared in this header file are responsible for setting up
 * signal handlers and handling the signals that are caught.
 */

/**
 * @brief Sets up the signal handlers for the process.
 *
 * This function configures the process to handle specific signals using the
 * `handle_sigint`, `handle_sigstop`, and `handle_sigchild` functions.
 *
 * @return An integer value representing the success or failure of setting up
 * the handlers.
 * @retval  0 If the setup is successful.
 */
int setup_handlers();

/**
 * @brief Handles the SIGCHLD signal.
 *
 * This function is called when a SIGCHLD signal is caught. It processes the
 * status of child processes and updates the job state accordingly.
 *
 * @param sig The signal number, which should be SIGCHLD.
 */
void handle_sigchild(int sig);

/**
 * @brief Handles the SIGINT signal.
 *
 * This function is called when a SIGINT signal is caught. It sends the signal
 * to the current job's process group.
 *
 * @param sig The signal number, which should be SIGINT.
 */
void handle_sigint(int sig);

/**
 * @brief Handles the SIGSTOP signal.
 *
 * This function is called when a SIGSTOP signal is caught. It sends the signal
 * to the current job's process group, updates the job state, and displays the
 * job information.
 *
 * @param sig The signal number, which should be SIGSTOP.
 */
void handle_sigstop(int sig);

#endif // !__HANDLERS_H
