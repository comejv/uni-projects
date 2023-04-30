#include <Python.h>
#include <stdlib.h>
#include <time.h>

static PyObject *c_unsat_clauses(PyObject *assignation, PyObject *cnf)
{
    PyObject *clauses, *unsat, *clause, *var;
    Py_ssize_t i, j;
    int clause_1;

    clauses = PyObject_CallMethod(cnf, "clauses", NULL);
    if (clauses == NULL)
    {
        return NULL;
    }

    unsat = PyList_New(0);
    if (unsat == NULL)
    {
        Py_DECREF(clauses);
        return NULL;
    }

    for (i = 0; i < PyList_Size(clauses); i++)
    {
        clause = PyList_GetItem(clauses, i);
        clause_1 = 0;

        for (j = 0; j < PyList_Size(clause); j++)
        {
            var = PyList_GetItem(clause, j);
            if (PySequence_Contains(assignation, var))
            {
                clause_1 = 1;
                break;
            }
        }

        if (!clause_1)
        {
            PyList_Append(unsat, clause);
        }
    }

    Py_DECREF(clauses);
    return unsat;
}


static double *c_jw_heuristic(PyObject *cnf)
{
    int nvars = PyLong_AsLong(PyObject_CallMethod(cnf, "nvars", NULL));

    PyObject *clauses = PyObject_CallMethod(cnf, "clauses", NULL);

    // Scores' end of array will be marked by 0
    double *scores = (double *)calloc(nvars + 2, sizeof(double));
    int total = 0;

    PyObject *clause_iter = PyObject_GetIter(clauses);
    PyObject *clause;
    while ((clause = PyIter_Next(clause_iter)) != NULL)
    {
        PyObject *var_iter = PyObject_GetIter(clause);
        PyObject *var_obj;
        while ((var_obj = PyIter_Next(var_iter)) != NULL)
        {
            int var = abs(PyLong_AsLong(var_obj));
            int clause_len = PyList_Size(clause);
            scores[var] += (double)clause_len;
            total += clause_len;
            Py_DECREF(var_obj);
        }
        Py_DECREF(var_iter);
        Py_DECREF(clause);
    }
    Py_DECREF(clause_iter);
    Py_DECREF(clauses);

    int new_total = 0;
    // Inverse scores
    for (int i = 1; i <= nvars; i++)
    {
        scores[i] = total - scores[i];
        new_total += (int)scores[i];
    }

    // Normalize and cumulative
    double cum_total = 0;
    for (int i = 1; i <= nvars; i++)
    {
        scores[i] = scores[i] / new_total;
        cum_total += scores[i];
        scores[i] = cum_total;
    }
    // Mark end of array
    scores[nvars + 1] = 0;

    return scores;
}


static int c_custom_random_choice(double *scores)
{
    double rand_num;

    rand_num = (double)rand() / RAND_MAX;

    for (int i = 0; scores[i] != 0; i++)
    {
        if (rand_num >= scores[i])
        {
            return i;
        }
    }
    return 1;
}

static PyObject *c_walk_sat(PyObject *self, PyObject *args)
{
    PyObject *cnf, *heuristic;
    if (!PyArg_ParseTuple(args, "O|Oi", &cnf, &heuristic))
    {
        return NULL;
    }

    // Run heuristic algorithm
    double *score = NULL;
    if (heuristic != Py_None)
    {
        PyObject *lower_heuristic = PyObject_CallMethod(heuristic, "lower", NULL);
        if (strcmp(PyUnicode_AsUTF8(lower_heuristic), "jw") == 0)
        {
            score = c_jw_heuristic(cnf);
        }
    }

    // Initialize the model
    PyObject *model = PyList_New(0);
    int nvars = PyLong_AsLong(PyObject_CallMethod(cnf, "nvars", NULL));
    for (int i = 1; i <= nvars; i++)
    {
        PyList_Append(model, PyLong_FromLong(i));
    }

    // Run the SAT solver
    int MAX_ITERATION = 100000;
    int n_iter = 0;
    int random_index;
    int y;
    double x;
    srand(time(NULL));
    while (n_iter < MAX_ITERATION)
    {
        // Get the list of unsatisfied clauses
        PyObject *clauses = c_unsat_clauses(model, cnf);

        // Get the number of unsatisfied clauses
        int clauses_size = PyList_Size(clauses);

        // If there are no unsatisfied clauses, return the model
        if (clauses_size == 0)
        {
            return model;
        }

        // Get a random unsatisfied clause
        random_index = rand() % clauses_size;
        PyObject *clause = PyList_GetItem(clauses, random_index);

        // Get a variable from the clause
        x = (double)rand() / RAND_MAX;
        if (x <= 0.6)
        {
            // Random choice
            random_index = rand() % PyList_Size(clause);
            y = abs(PyLong_AsLong(PyList_GetItem(clause, random_index)));
        }
        else
        {
            if (score != NULL)
            {
                // Deterministic choice (probability inverse of score)
                y = c_custom_random_choice(score);
            }
            else
            {
                y = abs(PyLong_AsLong(PyList_GetItem(clause, 0)));
            }
        }

        // Flip the variable
        int current_value = PyLong_AsLong(PyList_GetItem(model, y - 1));
        PyList_SetItem(model, y - 1, PyLong_FromLong(current_value * (-1)));
        n_iter++;
    }

    printf("Itération maximale atteinte\n");
    Py_RETURN_NONE;
}

/* Module method table */
static PyMethodDef c_sat_methods[] = {
    {"walk_sat", c_walk_sat, METH_VARARGS, "WalkSAT algorithm"},
    {NULL, NULL, 0, NULL} // Sentinel
};

/* Module definition */
static struct PyModuleDef sat_module = {
    PyModuleDef_HEAD_INIT,
    "Csat",       // Module name
    NULL,         // Module documentation (can be NULL)
    -1,           // Size of per-interpreter state (not needed, so -1)
    c_sat_methods // Module methods
};

/* Module initialization function */
PyMODINIT_FUNC PyInit_Csat(void)
{
    srand(time(NULL)); // Seed random number generator
    return PyModule_Create(&sat_module);
}
