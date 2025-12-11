/*overflowing.c*/
#include <stdio.h>
#include <string.h>



int verificar_login(char * usuario, char * senha)
{
	char buffer_user[0x10] = {0};
	char buffer_password[0x10] = {0};
	int autenticado = 0;

	strcpy(buffer_user, usuario);
	strcpy(buffer_password, senha);

	if (strcmp(buffer_user, "admin") == 0 &&
	    strcmp(buffer_password, "Ab123456") == 0){
		autenticado = 1;
	}

	return autenticado;
}

int main(int argc, char * argv[])
{
	if (argc != 3) 
	{
		printf("Uso: %s <usuario> <senha>\n", argv[0]);
		return 1;
	} 

	if (verificar_login(argv[1], argv[2]))
	{
		printf("Login bem sucedido!\n");
	}
	else{
		printf("Credenciais inválidas!\n");
	}

	return 0;
}
