/* File: example.i */
%module hashtable

%{
#define SWIG_FILE_WITH_INIT
#include "hashtable.h"
%}

%include "hashtable.h"
