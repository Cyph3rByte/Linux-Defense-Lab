# fuzz.py
import subprocess, sys



def check(length):
    payload = "A" * length
    try:

        res = subprocess.run(["./bin/vuln", "admin", payload], 
                           stdout=subprocess.PIPE, 
                           stderr=subprocess.PIPE)
        return res.returncode
    except:
        return -1

print("testando comprimento da senha...")


for i in range(16, 100, 8):
    ret = check(i)
    print(f"  tam {i}: ret {ret}")
    
    if ret not in [0, 1]:
        print(f"CRASH DETECTADO no tam {i} (código {ret})")
        break
