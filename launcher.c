#include <unistd.h>
#include <sys/wait.h>
#include <stdio.h>
#include <fcntl.h>

int main(int argc, char *argv[]) {
int cmd_pipe[2];
pipe(cmd_pipe);  // cmd_pipe[0] = baca, cmd_pipe[1] = tulis

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
        close(cmd_pipe[1]);              // child hanya baca
        dup2(cmd_pipe[0], STDIN_FILENO); // arahkan stdin ke pipe
        close(cmd_pipe[0]);

        argv[0] = "./TerrariaServer.bin.x86_64.real";
        execv(argv[0], argv);

        perror("exec Terraria failed");
        _exit(1);
    }

    pid_t p2 = fork();

    if (p2 == 0) {
        close(cmd_pipe[0]);              // logger hanya tulis
        dup2(cmd_pipe[1], STDOUT_FILENO); // logger "print" = kirim ke Terraria
        close(cmd_pipe[1]);

        execl("./logger", "logger", NULL);
        perror("exec logger failed");
        _exit(1);
    }
    
    close(cmd_pipe[0]);
    close(cmd_pipe[1]);

    waitpid(p, NULL, 0);
    waitpid(p2, NULL, 0);
    return 0;
}
