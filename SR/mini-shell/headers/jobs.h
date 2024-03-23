/**
 * @file jobs.h
 * @brief Defines data structures and functions related to managing background
 * jobs.
 */

#ifndef __JOBS_H
#define __JOBS_H

#include "csapp.h"
#include "linked_list.h"
#include "macro.h"

/**
 * @def N_MAX_JOBS
 * @brief Maximum number of jobs that can be managed concurrently.
 */
#define N_MAX_JOBS 10

/**
 * @typedef job_t
 * @brief Represents a running job in the shell.
 */
typedef struct job_t
{
    /**
     * @brief Unique identifier for the job.
     */
    int numero;

    /**
     * @brief Linked list containing process IDs (PIDs) associated with the job.
     */
    linkedList pids;

    /**
     * @brief Process group ID (GID) of the job.
     */
    gid_t gid;

    /**
     * @brief Current state of the job (RUNNING, STOPPED, TERMINATED).
     */
    int state;

    /**
     * @brief Complete command line used to launch the job.
     */
    char *command;
} job_t;

/**
 * @typedef job
 * @brief Type alias for a job_t pointer.
 */
typedef job_t *job;

/**
 * @brief Creates a copy of a command sequence string array.
 *
 * This function allocates memory and creates a single string by
 * concatenating the strings in the provided command sequence array.
 * It also inserts spaces between arguments and pipes.
 *
 * @param cmd_seq Pointer to an array of string arrays, where each inner
 *                array represents a command (the last string in each inner
 *                array is a null pointer).
 *
 * @return A newly allocated string representing the combined command,
 *         or NULL on error.
 */
char *copy_seq(char ***cmd_seq);

/**
 * @brief Prints information about a specific job.
 *
 * This function displays the job ID, its state, and the full command line
 * used to launch it.
 *
 * @param j Pointer to a job_t structure representing the job to display.
 */
void afficher_job(job j);

/**
 * @brief Lists all existing jobs with their details.
 *
 * This function iterates through the list of jobs and calls `afficher_job`
 * for each valid job entry.
 */
void list_jobs();

/**
 * @brief Creates a new job entry and adds it to the job list.
 *
 * This function takes information about the job's PIDs, GID, command line,
 * and initial state, and creates a new job_t structure. It then finds an
 * available slot in the `jobs` array and adds the new structure there.
 *
 * @param pids Linked list containing process IDs (PIDs) associated with the
 * job.
 * @param gid Process group ID (GID) of the job.
 * @param cmd_seq Pointer to an array of string arrays, where each inner
 *                array represents a command (the last string in each inner
 *                array is a null pointer).
 *
 * @return The ID of the newly created job, or -1 on error.
 */
int nouveau_job(linkedList pids, gid_t gid, char ***cmd_seq);

/**
 * @brief Frees the memory allocated for a job structure.
 *
 * This function releases the memory used by a job_t structure, including
 * its linked list of PIDs and the command line string.
 *
 * @param j Pointer to a job_t structure to be freed.
 */
void liberer_job(job j);

/**
 * @brief Brings a specific job to the foreground and continues its execution.
 *
 * This function checks if the specified job ID is valid and its state is
 * "STOPPED". If so, it sends a SIGCONT signal to the process group of the
 * job to resume its execution and updates the current job ID.
 *
 * @param job
 */
void fg_jobs(int job);

/**
 * @brief Sends a SIGCONT signal to the process group of a specific job,
 * resuming its execution if it was stopped.
 *
 * This function checks if the specified job ID is valid and its state is
 * "STOPPED". If so, it sends a SIGCONT signal to the process group of the
 * job to resume its execution.
 *
 * @param job ID of the job to resume.
 */
void bg_jobs(int job);

/**
 * @brief Sends a SIGTSTP signal to the process group of a specific job,
 * pausing its execution if it was running.
 *
 * This function checks if the specified job ID is valid and its state is
 * "RUNNING". If so, it sends a SIGTSTP signal to the process group of the
 * job to pause its execution.
 *
 * @param job ID of the job to pause.
 */
void stop_jobs(int job);

/**
 * @brief Waits for the currently running job to finish and cleans up its
 * resources.
 *
 * This function loops until the currently running job (identified by
 * `numero_job_courrant`) finishes execution. It then frees the memory
 * associated with the job and updates the `numero_job_courrant` variable.
 */
void attendre_job_courant();

/**
 * @brief Cleans up resources for any terminated jobs in the list.
 *
 * This function iterates through the list of jobs and checks if any job is
 * in the "TERMINATED" state. If so, it calls `liberer_job` to free its
 * associated resources and removes it from the list.
 */
void terminer_job();

#endif // __JOBS_H
