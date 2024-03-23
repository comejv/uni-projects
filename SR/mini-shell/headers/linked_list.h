/**
 * @file linked_list.h
 * @brief Defines functions and types for manipulating linked lists of integers.
 */

#ifndef __LINKED_LIST
#define __LINKED_LIST

#include <stdlib.h>
#include <stdio.h>
#include "csapp.h"
/**
 * @typedef node_t
 * @brief Structure representing a node in a linked list.
 *
 * This structure defines a node in a linked list of integers. Each node contains an
 * integer value and a pointer to the next node in the list.
 */
typedef struct node {
    pid_t pid;  /**< The integer value stored in the node. */
    struct node *next;  /**< Pointer to the next node in the list. */
} node_t;

/**
 * @typedef linkedList
 * @brief Type alias for a pointer to the first node in a linked list.
 *
 * This type alias simplifies the representation of a linked list by using a pointer
 * to the first node in the list.
 */
typedef node_t* linkedList;

/**
 * @brief Creates an empty linked list.
 *
 * This function allocates memory for a new empty linked list and returns a pointer
 * to the first node (which is always `NULL`).
 *
 * @return A pointer to the newly created empty linked list.
 */
linkedList listeVide();

/**
 * @brief Adds a new node containing the given value to the end of the list.
 *
 * This function inserts a new node with the specified value at the end of the
 * linked list. The function allocates memory for the new node and updates the
 * pointers in the list to maintain the correct linking.
 *
 * @param l Pointer to the head of the existing linked list.
 * @param value The integer value to insert into the new node.
 *
 * @return A pointer to the updated linked list (the same as the input parameter `l`).
 */
linkedList add(linkedList l, int value);

/**
 * @brief Removes the first node with the given value from the list.
 *
 * This function searches for the first node in the list that contains the specified
 * value and removes it. If the value is not found, the list remains unchanged. The
 * function frees the memory allocated for the removed node.
 *
 * @param l Pointer to the head of the existing linked list.
 * @param value The integer value to remove from the list.
 *
 * @return A pointer to the updated linked list (which may be different from the
 *         input parameter `l` if the node was removed).
 */
linkedList del(linkedList l, int value);

/**
 * @brief Checks if the list is empty.
 *
 * This function checks if the pointer to the first node in the list is `NULL`,
 * which indicates an empty list.
 *
 * @param l Pointer to the head of the linked list.
 *
 * @return 1 if the list is empty, 0 otherwise.
 */
int estVide(linkedList l);

/**
 * @brief Prints the values of all nodes in the list to the standard output.
 *
 * This function traverses the list and prints the value stored in each node to the
 * standard output.
 *
 * @param l Pointer to the head of the linked list.
 */
void affichage(linkedList l);

/**
 * @brief Frees the memory allocated for the linked list.
 *
 * This function traverses the list and frees the memory allocated for each node.
 * It is important to call this function to avoid memory leaks when you are finished
 * using the linked list.
 *
 * @param l Pointer to the head of the linked list.
 */
void libererListe(linkedList l);

/**
 * @brief Retrieves the value stored in the first node of the list.
 *
 * This function returns the value stored in the first node of the list. If the list
 * is empty, the function returns an undefined value.
 *
 * @param l Pointer to the head of the linked list.
 *
 * @return The value stored in the first node of the list (or an undefined value if
 *         the list is empty).
 */
int getValue(linkedList l);


#endif // __LINKED_LIST
