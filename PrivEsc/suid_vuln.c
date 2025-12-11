#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/types.h>

// Função vulnerável clássica
void bug(char *arg) {
    char buffer[64];
    strcpy(buffer, arg);
}

int main(int argc, char **argv) {
    // Mostra quem somos nós agora
    printf("[*] Processo iniciado.\n");
    printf("[*] Real UID: %d (Quem lançou)\n", getuid());
    printf("[*] Effective UID: %d (Poderes atuais)\n", geteuid());

    if (argc < 2) {
        printf("Uso: %s <payload>\n", argv[0]);
        exit(1);
    }

    // O bug acontece aqui
    bug(argv[1]);

    printf("[*] Fim normal (sem exploit).\n");
    return 0;
}
