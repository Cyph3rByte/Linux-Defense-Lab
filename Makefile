CC=gcc
SRC=overflowing.c
ADDR_SRC=get_addr.c
OUT_DIR=bin

all: clean vuln vuln32 nx canary pie secure addr_tools

prepare:
	mkdir -p $(OUT_DIR)

addr_tools: prepare
	$(CC) $(ADDR_SRC) -o $(OUT_DIR)/get_addr_64 -g
	$(CC) $(ADDR_SRC) -o $(OUT_DIR)/get_addr_32 -m32 -g

vuln: prepare
	$(CC) $(SRC) -o $(OUT_DIR)/vuln -fno-stack-protector -z execstack -no-pie -g

vuln32: prepare
	$(CC) $(SRC) -o $(OUT_DIR)/vuln32 -fno-stack-protector -z execstack -pie -fPIE -m32 -g

nx: prepare
	$(CC) $(SRC) -o $(OUT_DIR)/nx -fno-stack-protector -z noexecstack -no-pie -g

canary: prepare
	$(CC) $(SRC) -o $(OUT_DIR)/canary -fstack-protector-all -z execstack -no-pie -g

pie: prepare
	$(CC) $(SRC) -o $(OUT_DIR)/pie -fno-stack-protector -z execstack -pie -fPIE -g

secure: prepare
	$(CC) $(SRC) -o $(OUT_DIR)/secure -fstack-protector-all -z noexecstack -pie -fPIE -g

clean:
	rm -rf $(OUT_DIR)
