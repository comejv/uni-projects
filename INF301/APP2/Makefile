all: main


CC=clang

## Flags de compilation en mode debug, convient pour presque tout l'APP
CFLAGS= -g -Wall -Wextra -Werror -Wno-unused-parameter

## Flags de compilation pour les tests de performance.
## A decommenter pour desactiver tous les affichages, puis forcer la 
## recompilation avec 'make -B'
#CFLAGS=-O3 -g -Wall -Wextra -Werror -DSILENT -Wno-unused-parameter



# Ici, on utilise l'"intelligence" de 'make' qui saura tout seul
# comment créer les .o à partir des .c
main: main.o curiosity.o listes.o interprete.o type_pile.o


clean:
	rm -f main *.o
