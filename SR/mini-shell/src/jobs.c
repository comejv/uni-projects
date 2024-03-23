#include "jobs.h"
#include "global.h"

job *jobs = NULL; // Initialize with NULL for an empty list
int numero_job_courrant = -1;

char *copy_seq(char ***cmd_seq)
{
    int cmd_size = 1; // \0
    int i = 0, j = 0, k = 0;
    while (cmd_seq[i] != NULL)
    {
        j = 0;
        while (cmd_seq[i][j] != NULL)
        {
            k = 0;
            while (cmd_seq[i][j][k] != '\0')
            {
                cmd_size++;
                k++;
            }
            j++;
        }
        cmd_size += (j - 1); // space between each args
        i++;
    }
    cmd_size += (i - 1) * 3;
    char *command = malloc(sizeof(char) * cmd_size);
    if (command == NULL){
        perror("malloc");
        exit(EXIT_FAILURE);
    }
    int cmd_idx = 0;
    i = 0;
    while (cmd_seq[i] != NULL)
    {
        j = 0;
        while (cmd_seq[i][j] != NULL)
        {
            k = 0;
            while (cmd_seq[i][j][k] != '\0')
            {
                command[cmd_idx] = cmd_seq[i][j][k];
                cmd_idx++;
                k++;
            }
            if (cmd_seq[i][j + 1] != NULL)
            {
                command[cmd_idx] = ' ';
                cmd_idx++;
            }
            j++;
        }
        if (cmd_seq[i + 1] != NULL)
        {
            command[cmd_idx] = ' ';
            command[cmd_idx + 1] = '|';
            command[cmd_idx + 2] = ' ';
            cmd_idx += 3;
        }
        i++;
    }
    command[cmd_size - 1] = '\0';
    return command;
}

void afficher_job(job j)
{
    if (j)
    {
        printf("[%d] ", j->numero);
        switch (j->state)
        {
        case RUNNING:
            printf("En cours d'exécution");
            break;
        case STOPPED:
            printf("Arrêté");
            break;
        case TERMINATED:
            printf("Fini");
            break;
        }
        printf("    %s\n", j->command);
    }
}

void list_jobs()
{
    for (int i = 0; i < N_MAX_JOBS; i++)
    {
        afficher_job(jobs[i]);
    }
}

// Ajotue un nouveau job à la liste jobs
int nouveau_job(linkedList pids, gid_t gid, char ***cmd_seq)
{
    job new_job = (job)malloc(sizeof(job_t));
    if (new_job == NULL){
        perror("malloc");
        exit(EXIT_FAILURE);
    }
    new_job->command = copy_seq(cmd_seq);
    new_job->pids = pids;
    new_job->gid = gid;
    new_job->state = RUNNING;
    int job_id = N_MAX_JOBS - 1;
    while (job_id > 0 && jobs[job_id] == NULL)
    {
        job_id--;
    }
    job_id++;
    new_job->numero = job_id;
    DEBUG(JOBS, "Creating a new job at id %d\n", job_id);
    jobs[job_id] = new_job;
    return job_id;
}

// Libere la structure job
void liberer_job(job j)
{
    if (j)
    {
        libererListe(j->pids);
        free(j->command);
        free(j);
    }
}

// Passe un job voulu en fg
void fg_jobs(int job)
{
    if (job >= N_MAX_JOBS || job <= 0 || jobs[job] == NULL)
    {
        fprintf(stderr, "Error: invalid job number\n");
    }
    else if (jobs[job]->state == STOPPED)
    {
        DEBUG(JOBS, "Sending continue signal to GID:%d\n", jobs[job]->gid);
        Kill(-jobs[job]->gid, SIGCONT);
        jobs[job]->state = RUNNING;
        numero_job_courrant = job;
    }
    else if (jobs[job]->state == RUNNING)
    {
        numero_job_courrant = job;
    }
}

// Stop la pause du jobs voulu (initialement le dernier créé)
void bg_jobs(int job)
{
    if (job >= N_MAX_JOBS || job <= 0 || jobs[job] == NULL)
    {
        fprintf(stderr, "Error: invalid job number\n");
    }
    else if (jobs[job]->state == STOPPED)
    {
        DEBUG(JOBS, "Sending continue signal to GID:%d\n", jobs[job]->gid);
        Kill(-jobs[job]->gid, SIGCONT);
        jobs[job]->state = RUNNING;
    }
}

void stop_jobs(int job)
{
    if (job >= N_MAX_JOBS || job <= 0 || jobs[job] == NULL)
    {
        fprintf(stderr, "Error: invalid job number\n");
    }
    else if (jobs[job]->state == RUNNING)
    {
        DEBUG(JOBS, "Sending stop signal to GID:%d\n", jobs[job]->gid);
        Kill(-jobs[job]->gid, SIGTSTP);
    }
}

void attendre_job_courant()
{
    while (numero_job_courrant != -1 &&
           jobs[numero_job_courrant]->state != TERMINATED)
    {
        sleep(1);
    }
    if (numero_job_courrant != -1)
    {
        liberer_job(jobs[numero_job_courrant]);
        jobs[numero_job_courrant] = NULL;
    }
    numero_job_courrant = -1;
}

void terminer_job()
{
    for (int i = 0; i < N_MAX_JOBS; i++)
    {
        if (jobs[i] != NULL && jobs[i]->state == TERMINATED)
        {
            afficher_job(jobs[i]);
            liberer_job(jobs[i]);
            jobs[i] = NULL;
        }
    }
}
