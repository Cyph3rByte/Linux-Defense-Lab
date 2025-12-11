/* get_addr.c */

// Ajuda a imprimir o endereço de uma variável na pilha.
// Usado para demonstrar a entropia do ASLR.


#include <stdio.h>
#include <string.h>

int main() {
    char buffer[16];
    printf("%p\n", (void*)buffer);
    return 0;
}
