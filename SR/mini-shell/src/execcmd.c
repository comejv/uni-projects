#include "execcmd.h"
#include "global.h"
#include "jobs.h"
#include "linked_list.h"
#include "macro.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

int cd(char **cmd)
{
    char *path = malloc(sizeof(char) * MAXPATHLEN + 1);
    if (path == NULL)
        perror("malloc");
    if (!cmd[1])
    {
        char *temp = getenv("HOME");
        if (temp != NULL)
        {
            strncpy(path, temp, MAXPATHLEN);
        }
    }
    else if (cmd[1][0] == '~')
    {
        if (cmd[1][1] == '/' || cmd[1][1] == '\0')
        {
            char *temp = getenv("HOME");
            if (temp != NULL)
            {
                snprintf(path, MAXPATHLEN, "%s%s", temp, cmd[1] + 1);
            }
        }
        else
        {
            fprintf(stderr, "cd: syntaxe non supportée.\n");
        }
    }
    else
    {
        strncpy(path, cmd[1], MAXPATHLEN);
    }
    if (chdir(path))
    {
        fprintf(stderr, "chdir: %s: %s\n", strerror(errno), path);
        free(path);
        return 1;
    }
    char cwd[MAXPATHLEN];
    getcwd(cwd, MAXPATHLEN);
    setenv("PWD", cwd, 1);
    DEBUG(INTERNAL, "New dir : %s\n", getenv("PWD"));
    free(path);
    return 1;
}

int internal_cmd(char **cmd)
{
    if (cmd[0][0] == '#')
    {
        return 1;
    }
    if (!strcmp(cmd[0], "cd"))
    {
        DEBUG(INTERNAL, "cd command with arg %s\n", cmd[1]);
        return cd(cmd);
    }
    else if (!strcmp(cmd[0], "fg") || !strcmp(cmd[0], "bg") ||
             !strcmp(cmd[0], "stop"))
    {
        int job = 0;
        if (cmd[1] == NULL)
        {
            fprintf(stderr, "fg/bg/stop alone not implemented\n");
        }
        else if (cmd[1][0] == '%')
        {
            if (cmd[1] == NULL)
            {
                fprintf(stderr, "Need a job number !\n");
                return 1;
            }
            job = atoi(cmd[1] + 1);
            switch (cmd[0][0])
            {
            case 'f':
                fg_jobs(job);
                break;
            case 'b':
                bg_jobs(job);
                break;
            case 's':
                stop_jobs(job);
                break;
            }
        }
        else
        {
            fprintf(stderr, "Syntaxe non implémentée : %s\n", cmd[1]);
        }
        return 1;
    }
    else if (!strcmp(cmd[0], "jobs"))
    {
        list_jobs();
        return 1;
    }
    else if (!strcmp(cmd[0], "exit") || !strcmp(cmd[0], "quit"))
    {
        int ret = 0;
        if (cmd[1] != NULL)
        {
            ret = atoi(cmd[1]);
        }
        exit(ret);
    }
    return 0;
}

gid_t get_free_GID()
{
    gid_t gid = 1; // GID minimum possible
    // Tant que le groupe ID est déjà utilisé, continuer d'incrémenter
    while (getgrgid(gid) != NULL)
    {
        gid++;
    }
    return gid;
}

int compte_cmd(char ***seq)
{
    int i = 0;
    while (seq[i] != NULL)
    {
        i++;
    }
    return i;
}

int **create_pipes(int n_cmd)
{
    int **pipes = (int **)malloc(sizeof(int *) * n_cmd - 1);
    if (pipes == NULL)
    {
        perror("malloc");
        exit(EXIT_FAILURE);
    }
    for (int i = 0; i < n_cmd - 1; i++)
    {
        pipes[i] = (int *)malloc(sizeof(int) * 2);
        if (pipes[i] == NULL)
        {
            perror("malloc");
            exit(EXIT_FAILURE);
        }
        if (pipe(pipes[i]) == -1)
        {
            // pipe creation failed
            perror("pipe");
            exit(EXIT_FAILURE);
        }
    }
    return pipes;
}

void connection_pipes(int rang_cmd, int n_cmd, int **pipes)
{
    for (int pi = 0; pi < n_cmd - 1; pi++)
    {
        if (pi == rang_cmd)
        {
            DEBUG(PIPE, "Cmd n:%d fermeture pipes[%d][0]\n", rang_cmd, pi);
            DEBUG(PIPE, "Cmd n:%d new stdout pipes[%d][1]\n", rang_cmd, pi);
            if (dup2(pipes[pi][1], STDOUT_FILENO) == -1)
            {
                perror("dup2 in pipe");
                exit(EXIT_FAILURE);
            }
            close(pipes[pi][0]);
        }
        else if (pi == rang_cmd - 1)
        {
            DEBUG(PIPE, "Cmd n:%d fermeture pipes[%d][1]\n", rang_cmd, pi);
            DEBUG(PIPE, "Cmd n:%d new stdin pipes[%d][0]\n", rang_cmd, pi);
            if (dup2(pipes[pi][0], STDIN_FILENO) == -1)
            {
                perror("dup2 out pipe");
                exit(EXIT_FAILURE);
            }
            close(pipes[pi][1]);
        }
        else
        {
            DEBUG(PIPE, "Cmd n:%d fermeture pipes[%d][0]\n", rang_cmd, pi);
            DEBUG(PIPE, "Cmd n:%d fermeture pipes[%d][1]\n", rang_cmd, pi);
            close(pipes[pi][0]);
            close(pipes[pi][1]);
        }
    }
}

void free_pipes(int **pipes, int n_cmd)
{
    for (int i = 0; i < n_cmd - 1; i++)
    {
        free(pipes[i]);
    }
    free(pipes);
}

void connect_in_out(struct cmdline *l, int n_cmd, int current_commande_rank)
{
    if (current_commande_rank == 0 && l->in != NULL)
    {
        DEBUG(INOUT, "in: %s\n", l->in);
        int fd_in = open(l->in, O_RDONLY);
        if (fd_in == -1)
        {
            fprintf(stderr, "%s : Permission denied/file do not exist.\n",
                    l->in);
            exit(1);
        }
        if (dup2(fd_in, STDIN_FILENO) == -1){
            perror("dup2 in");
            exit(EXIT_FAILURE);
        };
    }
    if (current_commande_rank == n_cmd - 1 && l->out != NULL)
    {
        DEBUG(INOUT, "out: %s\n", l->out);
        int fd_out = open(l->out, O_WRONLY | O_CREAT, S_IRWXU);
        if (fd_out == -1)
        {
            fprintf(stderr, "%s : Permission denied.\n", l->out);
            exit(2);
        }
        if (dup2(fd_out, STDOUT_FILENO) == -1){
            perror("dup2 out");
            exit(EXIT_FAILURE);
        };
    }
}

void execution(struct cmdline *l)
{
    if (!l->seq[0])
        return;
    linkedList pids = listeVide();
    int n_cmd = compte_cmd(l->seq);
    int pid;
    int **pipes;
    gid_t gid = 0;
    if (n_cmd > 0)
    {
        pipes = create_pipes(n_cmd);
    }
    DEBUG(ALWAYS, "number of cmd:%d\n", n_cmd);
    DEBUG(JOBS, "Is background :%s\n", l->bg ? "yes" : "no");
    int internals = 0;
    for (int i = 0; i < n_cmd; i++)
    {
        if (internal_cmd(l->seq[i]))
        {
            internals++;
            continue;
        }
        pid = Fork();
        if (pid == -1)
        {
            perror("fork");
        }
        else if (pid != 0) // Parent
        {
            if (gid == 0)
            {
                gid = pid;
            }
            setpgid(pid, gid);
            pids = add(pids, pid);
        }
        else // Fils
        {
            connect_in_out(l, n_cmd, i);
            DEBUG(JOBS, "Execution commande : %s\n", l->seq[i][0]);
            connection_pipes(i, n_cmd, pipes);
            free_pipes(pipes, n_cmd); // Avoid memory leaks
            if (execvp(l->seq[i][0], l->seq[i]) == -1)
            {
                printf("%s : command not found\n", l->seq[i][0]);
                exit(3);
            }
        }
    }
    connection_pipes(-1, n_cmd, pipes); // -1 afin de fermer tout les pipes
    free_pipes(pipes, n_cmd);           // Avoid memory leaks
    if (internals == n_cmd)             // Si seulement commandes internes
    {
        return;
    }
    // create_job
    int job_id = nouveau_job(pids, gid, l->seq);
    if (!l->bg)
    {
        numero_job_courrant = job_id;
    }
    return;
}
