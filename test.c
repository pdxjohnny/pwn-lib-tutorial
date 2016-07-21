#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

const char binsh[] = "/bin/sh";

int gtfo(const char *filename, char *const argv[], char *const envp[]) {
    return execve(filename, argv, envp);
}

int main(int agrv, char ** argc) {
    return gtfo(binsh, NULL, NULL);
}
