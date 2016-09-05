run: compile
	sudo ./lab

compile: pcap.c pcap.h
	gcc pcap.c -o lab -lpcap