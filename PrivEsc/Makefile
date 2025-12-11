CC = gcc
CFLAGS = -fno-stack-protector -z execstack -no-pie -m64

all: suid_vuln

suid_vuln: suid_vuln.c
	$(CC) $(CFLAGS) -o suid_vuln suid_vuln.c

clean:
	rm -f suid_vuln
