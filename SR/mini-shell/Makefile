.PHONY: all clean doc ensureDirs systests

# Disable implicit rules
.SUFFIXES:

CC = gcc
CFLAGS = -Wall -Wextra -g
CPPFLAGS =

# Note: -lnsl does not seem to work on Mac OS but will
SRCDIR = src
OBJDIR = obj
EXECDIR = .
HEADERSDIR = headers
CPPFLAGS += -I$(HEADERSDIR)
DOCDIR = doc
DOCCONF = doxy-convert.conf

SRCS = $(wildcard $(SRCDIR)/*.c)
HEADERS = $(wildcard $(HEADERSDIR)/*.h)
OBJS = $(SRCS:$(SRCDIR)/%.c=$(OBJDIR)/%.o)
MAIN_OBJ = $(OBJDIR)/shell.o
EXEC = $(MAIN_OBJ:$(OBJDIR)%.o=$(EXECDIR)/%)

# probably be necessary on Solaris for linking network-related functions 
#LIBS += -lsocket -lnsl -lrt
LDFLAGS += -lpthread

ifdef DEBUG 
CPPFLAGS += -fsanitize=address -fsanitize-recover -fno-omit-frame-pointer
CFLAGS += -g -fsanitize=address -fsanitize-recover -fno-omit-frame-pointer
LDFLAGS += -fsanitize=address
ifeq ($(DEBUG),PIPE)
CPPFLAGS += -DFDEBUG=1
else ifeq ($(DEBUG),INOUT)
CPPFLAGS += -DFDEBUG=2
else ifeq ($(DEBUG),JOBS)
CPPFLAGS += -DFDEBUG=3
else ifeq ($(DEBUG),INTERNAL)
CPPFLAGS += -DFDEBUG=4
else
CPPFLAGS += -DFDEBUG=0
endif
else
# ASAN crashed randomly, do not use
ifdef ASAN
CFLAGS += -g -fsanitize=address -fsanitize=undefined -fsanitize-recover -fno-omit-frame-pointer
LDFLAGS += -fsanitize=address -fsanitize=undefined
endif
endif

ifdef TESTS
CPPFLAGS += -DQUIET
OPTGCOV = -fprofile-arcs -ftest-coverage
CFLAGS += $(OPTGCOV)
LDFLAGS += $(OPTGCOV) -lgcov
endif

all: ensureDirs $(EXEC)

# Rule to make the object files
$(OBJDIR)/%.o:$(SRCDIR)/%.c
	$(CC) $(CFLAGS) $(CPPFLAGS) -c $< -o $@ $()

$(OBJDIR)/readcmd.o : $(HEADERSDIR)/readcmd.h
$(OBJDIR)/execcmd.o : $(HEADERSDIR)/execcmd.h
$(OBJDIR)/jobs.o : $(HEADERSDIR)/jobs.h
$(OBJDIR)/handlers.o : $(HEADERSDIR)/handlers.h 
$(OBJDIR)/linked_list.o : $(HEADERSDIR)/linked_list.h
$(MAIN_OBJ) : $(HEADERS)

$(EXEC) : $(OBJS)
	$(CC) $(OBJS) -o $@ $(LDFLAGS)

systests :
	$(MAKE) clean
	$(CC) tests/custom_sdriver.c -o tests/$@
	$(MAKE) TESTS=1 # ASAN=1
	bash tests/systests.bash tests/shell_scripts/*

showGcov:
	@gcov -b -o $(OBJDIR) -c $(SRCDIR)/execcmd.c $(SRCDIR)/readcmd.c $(SRCDIR)/handlers.c $(SRCDIR)/jobs.c $(SRCDIR)/shell.c

doc:
	@echo
	@echo "----- Creating documentation -----"
	cd $(DOCDIR); \
	doxygen $(DOCCONF)

ensureDirs:
	@echo "----- Main compilation -----"

	@mkdir -p $(OBJDIR)
	@mkdir -p $(EXECDIR)
	@mkdir -p $(DOCDIR)

clean:
	-rm -f shell $(OBJS) custom_sdriver
	-rm $(OBJDIR)/*.gc* 2> /dev/null
	-rm *.gcov
	-rm -rf $(DOCDIR)/html $(DOCDIR)/latex

