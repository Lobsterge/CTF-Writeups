#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <sys/wait.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <unistd.h>

#include <errno.h>
#include <linux/audit.h>
#include <linux/bpf.h>
#include <linux/filter.h>
#include <linux/seccomp.h>
#include <linux/unistd.h>
#include <stddef.h>
#include <stdio.h>
#include <sys/prctl.h>
#include <unistd.h>

#include <stdbool.h>

bool install_filter()
{
	struct sock_filter filter[] = {
		BPF_STMT(BPF_LD + BPF_W + BPF_ABS, (offsetof(struct seccomp_data, arch))),
		BPF_JUMP(BPF_JMP + BPF_JEQ + BPF_K, AUDIT_ARCH_X86_64, 1, 0),
		BPF_STMT(BPF_RET + BPF_K, SECCOMP_RET_KILL_PROCESS),

		BPF_STMT(BPF_LD + BPF_W + BPF_ABS, (offsetof(struct seccomp_data, nr))),

		BPF_JUMP(BPF_JMP + BPF_JEQ + BPF_K, __NR_write, 0, 1),
		BPF_STMT(BPF_RET + BPF_K, SECCOMP_RET_ALLOW),
		BPF_JUMP(BPF_JMP + BPF_JEQ + BPF_K, __NR_exit, 0, 1),
		BPF_STMT(BPF_RET + BPF_K, SECCOMP_RET_ALLOW),
		BPF_JUMP(BPF_JMP + BPF_JEQ + BPF_K, __NR_exit_group, 0, 1),
		BPF_STMT(BPF_RET + BPF_K, SECCOMP_RET_ALLOW),
		BPF_STMT(BPF_RET + BPF_K, SECCOMP_RET_KILL_PROCESS),
	};
	struct sock_fprog prog = {
		.len = (unsigned short)(sizeof(filter) / sizeof(filter[0])),
		.filter = filter,
	};
	if (prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0))
	{
		perror("prctl(NO_NEW_PRIVS)");
		return 1;
	}
	if (prctl(PR_SET_SECCOMP, 2, &prog))
	{
		perror("prctl(PR_SET_SECCOMP)");
		return 1;
	}
	return 0;
}

int main()
{
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);

	const int FLAG_SIZE = 0x40;
	char flag[FLAG_SIZE];
	char *flag_mem = (char *)mmap(NULL, FLAG_SIZE, PROT_WRITE, MAP_ANONYMOUS | MAP_PRIVATE, -1, 0);
	FILE *flag_file = fopen("flag", "r");
	fread(flag_mem, 1, FLAG_SIZE, flag_file);
	fclose(flag_file);

	const int CODE_SIZE = 0x200;
	char *code_mem = (char *)mmap(NULL, CODE_SIZE, PROT_READ | PROT_WRITE, MAP_ANONYMOUS | MAP_PRIVATE, -1, 0);
	read(STDIN_FILENO, code_mem, CODE_SIZE);
	mprotect(code_mem, CODE_SIZE, PROT_READ | PROT_EXEC);

	install_filter();

	asm(
		"mov rax, %0;" // flag address in rax
		"jmp %1;"	   // jump into recdeived code
		:			   // no output
		: "r"(flag_mem), "r"(code_mem));
}
