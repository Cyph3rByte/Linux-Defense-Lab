# Linux Defense Lab

```
              .,,uod8B8bou,,.
              ..,uod8BBBBBBBBBBBBBBBBRPFT?l!i:.
         ,=m8BBBBBBBBBBBBBBBRPFT?!||||||||||||||
         !...:!TVBBBRPFT||||||||||!!^^""'   ||||
         !.......:!?|||||!!^^""'            ||||
         !.........||||                     ||||
         !.........||||  ##                 ||||
         !.........||||                     ||||
         !.........||||                     ||||
         !.........||||                     ||||
         !.........||||                     ||||
         `.........||||                    ,||||
          .;.......||||               _.-!!|||||
   .,uodWBBBBb.....||||       _.-!!|||||||||!:'
!YBBBBBBBBBBBBBBb..!|||:..-!!|||||||!iof68BBBBBb....
!..YBBBBBBBBBBBBBBb!!||||||||!iof68BBBBBBRPFT?!::   `.
!....YBBBBBBBBBBBBBBbaaitf68BBBBBBRPFT?!:::::::::     `.
!......YBBBBBBBBBBBBBBBBBBBRPFT?!::::::;:!^"`;:::       `.
!........YBBBBBBBBBBRPFT?!::::::::::^''...::::::;         iBBbo.
`..........YBRPFT?!::::::::::::::::::::::::;iof68bo.      WBBBBbo.
```

Este repositório contém o código fonte e scripts desenvolvido para o nosso artigo sobre mecanismos de defesa em Sistemas Operacionais. A ideia aqui foi criar um laboratório prático para testar se proteções como NX, Canary e ASLR realmente seguram o tranco contra ataques clássicos de Buffer Overflow.

O projeto ainda está em andamento, então devo subir mais atualizações conforme a gente for avançando na pesquisa (especialmente na parte de escalonamento de privilégios).

## Cenário Experimental

Rodamos os testes em dois ambientes virtualizados (VirtualBox). Se for rodar em outro lugar, talvez precise ajustar os offsets no código:

1.  **VM Vulnerável**:
    *   OS: Ubuntu 22.04.5 LTS x86_64
    *   Kernel: 6.8.0-87-generic
    *   Configuração: ASLR=0, Sem Canary, Sem NX, Sem PIE.

2.  **VM Segura**:
    *   OS: CentOS Stream 10 x86_64
    *   Kernel: 6.12.0-164.0e10.x86_64
    *   Configuração: ASLR=2, Canary, NX, PIE, SELinux.

## Requisitos

*   Linux x86_64
*   GCC (precisa do `gcc-multilib` para os testes de 32-bit)
*   Python 3
*   `make` e `setarch`

## Estrutura do Projeto

*   `overflowing.c`: O código vulnerável (strcpy clássico).
*   `PrivEsc/`: Pasta com os testes de escalonamento de privilégios (SUID).
*   `benchmark.py`: Script principal que automatiza os ataques e gera as estatísticas.
*   `exploit_*.py`: Scripts individuais para testar cada cenário manualmente.

## Como Reproduzir

### 1. Compilação

Só rodar o make na raiz:

```bash
make all
```

### 2. Rodando o Benchmark

Para gerar os dados que usamos no artigo:

```bash
python3 benchmark.py
```

O script vai calibrar o offset da pilha sozinho e tentar explorar os binários em diferentes configurações. Ele também roda um bruteforce em 32-bit para mostrar como o ASLR é fraco nessa arquitetura.

### 3. Testando Escalonamento (PrivEsc)

Para ver a diferença que as permissões fazem:

```bash
cd PrivEsc
make
# Simule um erro de admin
sudo chown root:root suid_vuln
sudo chmod u+s suid_vuln
# Ataque
python3 exploit_privesc.py
```

Se tudo der certo, você deve pegar um shell root.
