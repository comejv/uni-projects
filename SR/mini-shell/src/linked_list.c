#include "linked_list.h"

linkedList listeVide()
{
    return NULL;
}

linkedList add(linkedList l, pid_t pid)
{
    linkedList new_l = malloc(sizeof(node_t));
    if (new_l == NULL){
        perror("malloc");
        exit(EXIT_FAILURE);
    }
    new_l->next = l;
    new_l->pid = pid;
    return new_l;
}

linkedList del(linkedList l, pid_t pid)
{
    linkedList prev = NULL;
    linkedList curr = l;

    while (curr != NULL && curr->pid != pid)
    {
        prev = curr;
        curr = curr->next;
    }

    if (curr == NULL)
    {
        // L'élément à supprimer n'a pas été trouvé
        return l;
    }

    if (prev == NULL)
    {
        // L'élément à supprimer est le premier de la liste
        l = curr->next;
    }
    else
    {
        prev->next = curr->next;
    }

    free(curr);
    return l;
}

int estVide(linkedList l)
{
    return l == NULL;
}

void affichage(linkedList l)
{
    while (l != NULL)
    {
        printf("%d -> ", l->pid);
        l = l->next;
    }
}

void libererListe(linkedList l)
{
    linkedList p = NULL;
    while (l)
    {
        p = l;
        l = l->next;
        free(p);
    }
    return;
}

int getValue(linkedList l)
{
    if (l)
    {
        return l->pid;
    }
    return -1;
}

void envoie_signal(linkedList l, int signum)
{
    while (l)
    {
        Kill(l->pid, signum);
        l = l->next;
    }
}