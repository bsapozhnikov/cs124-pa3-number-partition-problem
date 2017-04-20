#include <stdio.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
  char *py_argv[4];
  py_argv[0] = "python";
  py_argv[1] = "./kk.py";
  py_argv[2] = argc > 1 ? argv[1] : NULL;
  py_argv[3] = NULL;
  execvp("python", py_argv);
}
