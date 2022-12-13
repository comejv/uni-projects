CC=clang -Wall -g -Wno-switch

PROGRAMMES=test_terrain test_robot robot_terrain curiosity oracle_interprete test_generation_terrains curiosity_perfs

all: $(PROGRAMMES) clean

######################################################################
#                       Règles de compilation                        #
######################################################################

%.o: %.c
	$(CC) -c $<

test_terrain.o: test_terrain.c terrain.h

test_robot.o: test_robot.c robot.h

robot_terrain.o: robot_terrain.c terrain.h robot.h

robot.o: robot.c robot.h

terrain.o: terrain.c terrain.h

observateur.o: observateur.c observateur.h

environnement.o: environnement.c environnement.h robot.h terrain.h observateur.h

programme.o: programme.c programme.h type_pile.h

interprete.o: interprete.c interprete.h environnement.h \
	programme.h type_pile.h robot.h terrain.h

interprete%.o: interprete%.c interprete.h environnement.h \
	programme.h type_pile.h robot.h terrain.h

type_pile.o: type_pile.c type_pile.h

curiosity.o: curiosity.c environnement.h programme.h \
	interprete.h robot.h terrain.h type_pile.h observateur.h

oracle_interprete.o: oracle_interprete.c oracle_interprete.h \
	interprete.h environnement.h programme.h type_pile.h robot.h terrain.h

generation_terrains.o: generation_terrains.c generation_terrains.h

test_generation_terrains.o: test_generation_terrains.c generation_terrains.h terrain.h

curiosity_perfs.o: curiosity_perfs.c environnement.h programme.h \
	interprete.h generation_terrains.h

######################################################################
#                       Règles d'édition de liens                    #
######################################################################

test_terrain: test_terrain.o terrain.o
	$(CC) $^ -o $@

test_robot: test_robot.o robot.o
	$(CC) $^ -o $@

robot_terrain: robot_terrain.o terrain.o robot.o
	$(CC) $^ -o $@

curiosity: curiosity.o environnement.o programme.o interprete.o \
	robot.o terrain.o type_pile.o observateur.o
	$(CC) $^ -o $@

oracle_interprete: oracle_interprete.o interprete.o environnement.o \
	programme.o type_pile.o robot.o terrain.o observateur.o
	$(CC) $^ -o $@

oracle_interprete%: oracle_interprete.o interprete%.o environnement.o \
	programme.o type_pile.o robot.o terrain.o observateur.o
	$(CC) $^ -o $@

test_generation_terrains: test_generation_terrains.o generation_terrains.o terrain.o
	$(CC) $^ -o $@

curiosity_perfs: curiosity_perfs.o environnement.o programme.o interprete.o \
	robot.o terrain.o type_pile.o generation_terrains.o observateur.o
	$(CC) $^ -o $@

clean:
	rm -f *.o

clear:clean
	rm -f $(PROGRAMMES)


tests:
	for f in ./tests/*.test; do ./oracle_interprete $$f; done;

.PHONY: clean clear tests