/*
 * Copyright (C) 2002, Simon Nieuviarts
 */
#include "execcmd.h"
#include "global.h"
#include "handlers.h"
#include "readcmd.h"
#include <stdio.h>
#include <stdlib.h>

int main()
{
    jobs = (job *)calloc(N_MAX_JOBS, sizeof(job));
    if (jobs == NULL)
    {
        perror("malloc");
        exit(EXIT_FAILURE);
    }
    numero_job_courrant = -1;
    setup_handlers();
    struct cmdline *l;
    while (1)
    {
        // list_jobs();
#ifndef QUIET
        printf("mini-shell:%s> ", getenv("PWD"));
        terminer_job();
#endif /* ifndef QUIET  */
        l = readcmd();
        if (!l)
        {
#ifndef QUIET
            printf("bye bye\n");
#endif /* ifndef QUIET */
            exit(0);
        }
        if (l->err)
        {
            /* Syntax error, read another command */
            fprintf(stderr, "error: %s\n", l->err);
            continue;
        }
        execution(l);
        attendre_job_courant();
    }
}
