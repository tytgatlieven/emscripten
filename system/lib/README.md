Source code for C/C++ system libaries
=====================================

This directory contains the source code for libc, libc++ and other C/C++ system
libraries.  Where possible these are clones of upstream projects (e.g. musl).
For more details about each library see the individual readme files in the
subdirectoris.

Static constructor ordering
---------------------------

These are several static constructors in the emscripten system libraries and they
are in a specific order.  When adding/remove/updating these please update this
document.

These current set of static constructors in system libraries and their priorities
(lowest run first) are:

- 47: `initialize_emmalloc_heap` (emmalloc.c)
- 48: `__emscripten_pthread_data_constructor` (pthread/emscripten_tls_init.c)
- 49: `emscripten_tls_init` (pthread/library_pthread.c)
- 50: asan init (??)

Priorities 0 - 100 are reserved for system libraries and user-level
constructors should all run at 101 and above (for example libc++ initializes
its standard I/O streams at priority 101).
