#include <unistd.h>
#include <sys/wait.h>
#include <stdio.h>
#include <fcntl.h>

int main(int argc, char *argv[]) {

    pid_t p = fork();

    if (p == 0) {
        // CHILD 1: run Terraria + save log as Terraria.log

        int fd = open("Terraria.log",
                      O_CREAT | O_WRONLY | O_APPEND,
                      0644);

        if (fd < 0) {
            perror("open Terraria.log failed");
            _exit(1);
        }

        // stdout and stderr >>> file
        dup2(fd, STDOUT_FILENO);
        dup2(fd, STDERR_FILENO);
        close(fd);

        execv("./TerrariaServer.bin.x86_64.real", argv);

        perror("exec Terraria failed");
        _exit(1);
    }

    pid_t p2 = fork();

    if (p2 == 0) {
        execl("./logger", "logger", NULL);
        perror("exec logger failed");
        _exit(1);
    }

    waitpid(p, NULL, 0);
    waitpid(p2, NULL, 0);
    return 0;
}
