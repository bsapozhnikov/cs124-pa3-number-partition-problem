#include <stdio.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
  if (argc < 2) {
    printf("Usage: ./kk inputfile\n");
    return 1;
  }
  char *py_argv[3];
  py_argv[0] = "python";
  py_argv[1] = "./kk.py";
  py_argv[2] = argv[1];
  execvp("python", py_argv);
}
