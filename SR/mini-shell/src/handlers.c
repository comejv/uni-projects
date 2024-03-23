#include "handlers.h"

void handle_sigchild(int sig)
{
    pid_t pid;
    int status;
    while ((pid = waitpid(-1, &status, WNOHANG | WUNTRACED)) > 0)
    {
        DEBUG(JOBS, "Child %d sent a signal\n", pid);
        if (WIFEXITED(status) || WIFSIGNALED(status))
        {
            DEBUG(JOBS, "Child %d exited\n", pid);
            for (int i = 0; i < N_MAX_JOBS; i++)
            {
                if (jobs[i] != NULL)
                {
                    jobs[i]->pids = del(jobs[i]->pids, pid);
                    if (jobs[i]->pids == NULL)
                    {
                        jobs[i]->state = TERMINATED;
                    }
                }
            }
        }
        else if (WIFSTOPPED(status))
        {
            DEBUG(JOBS, "Child %d stopped by sig %d\n", pid, WSTOPSIG(status));
            gid_t gid = getpgid(pid);
            for (int i = 0; i < N_MAX_JOBS; i++){
                if (jobs[i] != NULL && jobs[i]->gid == gid){
                    jobs[i]->state = STOPPED;
                    printf("\n");
                    afficher_job(jobs[numero_job_courrant]);
                    numero_job_courrant = -1;
                }
            }
        }
    }
    return;
}

void handle_sigclavier(int sig)
{
    if (numero_job_courrant != -1)
    {
        kill(-jobs[numero_job_courrant]->gid, sig);
    }
    return;
}

int setup_handlers()
{
    Signal(SIGINT, handle_sigclavier);
    Signal(SIGTSTP, handle_sigclavier);
    Signal(SIGCHLD, handle_sigchild);
    return 0;
}
