#include <iostream>
#include <iomanip>
#include <map>
#include <vector>
#include <cstring>

#include <sys/mman.h>

using std::vector, std::map, std::string;

using byte = unsigned char;

template<typename T>
void vector_append(vector<T>& into, const vector<T>& from) {
	into.insert(into.end(), from.begin(), from.end());
}

vector<byte> compile(const string& code) {
	vector<byte> compiled;
	const map<char, vector<byte>> instructions = {
		{'>', {0x48, 0xff, 0xc3}}, // ptr++ -> inc rbx;
		{'<', {0x48, 0xff, 0xcb}}, // ptr-- -> dec rbx;
		{'+', {0xfe, 0x03}}, // *ptr++ -> inc byte ptr [rbx];
		{'-', {0xfe, 0x0b}}, // *ptr-- -> dec byte ptr [rbx];
		{'.',
			{
				0x48, 0x31, 0xc0, 0xb0, 0x01, // xor rax, rax; mov al, 1; (rax = 1 - syscall: write)
				0x48, 0xc7, 0xc7, 0x01, 0x00, 0x00, 0x00, // mov rdi, 1; (rdi = 1 - fd: stdout)
				0x48, 0x89, 0xde, // mov rsi, rbx; (rsi = rbx - buff: current char)
				0x48, 0x31, 0xd2, 0xb2, 0x01, // xor rdx, rdx; mov dl, 1; (rdx = 1 - count: 1)
				0x0f, 0x05 // syscall - write(stdou, rbx, 1)
			}}, // putc(*ptr)
	};
	const vector<byte> compiled_end = {
		0x48, 0xC7, 0xC0, 0x3C, 0x00, 0x00, 0x00, // mov rax, 0x3c
		0x0F, 0x05 // syscall (exit())
	};
	for (char c: code) {
		auto found_instruction = instructions.find(c);
		if(found_instruction != instructions.end()) {
			vector_append<>(compiled, found_instruction->second);
		}
	}
	vector_append(compiled, compiled_end);
	return compiled;
}

std::string read_code() {
	std::string code;
	std::cin >> std::setw(0x4000) >> code;
	return code;
}

void print_instruction() {
	std::setbuf(stdin, nullptr);
	std::setbuf(stdout, nullptr);

	std::cout << "Welcome to blazing fast brainfuck compiler!\n";
	std::cout << "Compile your brainfuck code into highly optimized native code to execute your brainfuck code faster then ever!\n";
	std::cout << "(note that jump instructions have been removed, to make sure all programs terminate ";
	std::cout << "but that means that it's very secure!)\n";

	std::cout << "Example program:\n";
	std::cout << "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++>";
	std::cout << "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++>";
	std::cout << "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++";
	std::cout << "<<.>>.<.<.\n";

	std::cout << "Enter your code:\n";
}

void execute_code(vector<byte> compiled) {
	const int DATA_SIZE = 0x200;
	char* code_mem = (char*) mmap(nullptr, compiled.size() + DATA_SIZE, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_PRIVATE | MAP_ANONYMOUS, 0, 0);
	std::memcpy(code_mem, compiled.data(), compiled.size());
	char* data_mem = code_mem + compiled.size();

	asm (
			"mov rbx, %0;" // data pointer stored in rbx
			"jmp %1;" // jump into compiled code
			: // no output
			: "r" (data_mem), "r" (code_mem)
		);
}

int main() {
	print_instruction();
	vector<byte> compiled_code = compile(read_code());
	execute_code(compiled_code);
}

