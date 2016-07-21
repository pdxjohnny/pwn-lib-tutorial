#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define INPUT_SIZE 200
void input(char * buffer);
const char binsh[] = "/bin/sh";

int gtfo(const char *filename, char *const argv[], char *const envp[]) {
    return execve(filename, argv, envp);
}

void input(char * buffer) {
    read(STDIN_FILENO, buffer, INPUT_SIZE);
    return;
}

int main(int agrv, char ** argc) {
    // char msg[11];
    // memset(msg, 'G', 11);
    // input(msg);
    // printf("%s", msg);
    gtfo(binsh, NULL, NULL);
    return EXIT_SUCCESS;
}
