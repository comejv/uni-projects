/**
 * @file macro.h
 * @brief Defines utility macros.
 */

#ifndef __MACRO_H
#define __MACRO_H

/**
 * @def DEBUG(feat, ...)
 * @brief Conditional debug macro.
 *
 * This macro conditionally prints debug information to the standard error
 * stream. The information printed includes the source file name, line number,
 * and the formatted arguments provided to the macro.
 *
 * @param feat Defines which debug messages will be shown (0 for all messages)
 * @param ... Variable number of arguments to be formatted and printed.
 *
 * @note The behavior of this macro depends on the existence of a preprocessor
 * symbol named `FDEBUG`. If `FDEBUG` is defined, the messages whose `feat`
 * parameter matches the value of the `FDEBUG` macro will be shown. The `FDEBUG`
 * macro is defined in the Makefile, depends on the value of the `DEBUG`
 * parameter given when calling make. Otherwise, the macro does nothing.
 *
 * @example
 *
 * If `FDEBUG` is defined by compiling with `make DEBUG=PIPE`:
 *
 * ```c
 * DEBUG(PIPE, "Entering function %s\n", __func__);
 * ```
 *
 * would print the following to the standard error stream:
 *
 * ```
 * macro.h:13 -> Entering function my_function
 * ```
 *
 * But this message would not be printed due to its `feat` parameter not
 * matching the FDEBUG parameter :
 *
 * ```c
 * DEBUG(JOBS, "Calling job %d", 3)
 * ```
 */
#ifdef FDEBUG
#define DEBUG(feat, ...)                                                       \
    do                                                                         \
    {                                                                          \
        if (!FDEBUG || !feat || feat == FDEBUG)                                \
        {                                                                      \
            fprintf(stderr, "%s:%d -> ", __FILE__, __LINE__);                  \
            fprintf(stderr, __VA_ARGS__);                                      \
            fflush(stderr);                                                    \
        }                                                                      \
    } while (0)
#else
#define DEBUG(...)                                                             \
    do                                                                         \
    {                                                                          \
    } while (0)
#endif // FDEBUG

#define ALWAYS 0
#define PIPE 1
#define INOUT 2
#define JOBS 3
#define INTERNAL 4

#endif // __MACRO_H
