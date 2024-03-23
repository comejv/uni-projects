/**
 * @file global.h
 * @brief Declares global variables and functions for process management.
 *
 * @include linked_list.h
 */

#ifndef __GLOBAL_H
#define __GLOBAL_H
#include "linked_list.h"
#include "jobs.h"
#define RUNNING 0
#define STOPPED 1
#define TERMINATED 2 
#define FOREGROUND 3
#define BACKGROUND 4

/**
 * @var jobs
 * @brief A list of the current running jobs 
 *
 */
extern job* jobs;

/**
 * @var numero_job_courrant
 * @brief jobs[numero_job_courrant] = foreground job 
 * 
 */
extern int numero_job_courrant;

#endif // __GLOBAL_H
