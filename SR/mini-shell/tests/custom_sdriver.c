#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

int main(int argc, char *argv[])
{
    if (argc != 3)
    {
        fprintf(stderr, "Usage: %s <shell> <file>\n", argv[0]);
        exit(1);
    }

    FILE *fp = fopen(argv[2], "r");
    if (fp == NULL)
    {
        perror("fopen");
        exit(1);
    }

    pid_t pid = fork();
    if (pid < 0)
    {
        perror("fork");
        exit(1);
    }
    else if (pid == 0)
    {                                   // Child process
        dup2(fileno(fp), STDIN_FILENO); // Redirect stdin to the file
        execl(argv[1], "shell", NULL);  // Execute the shell program
        perror("execl");
        exit(1);
    }
    else
    { // Parent process
        // Wait for the child process to finish
        waitpid(pid, NULL, 0);
        fclose(fp); // Close the file in the parent process
    }

    return 0;
}
