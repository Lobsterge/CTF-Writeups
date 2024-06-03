
void _DT_INIT(void)

{
  __gmon_start__();
  return;
}



void FUN_00101020(void)

{
                    /* WARNING: Treating indirect jump as call */
  (*(code *)(undefined *)0x0)();
  return;
}



/* WARNING: Unknown calling convention -- yet parameter storage is locked */

void free(void *__ptr)

{
  free(__ptr);
  return;
}



/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int puts(char *__s)

{
  int iVar1;
  
  iVar1 = puts(__s);
  return iVar1;
}



/* WARNING: Unknown calling convention -- yet parameter storage is locked */

ssize_t write(int __fd,void *__buf,size_t __n)

{
  ssize_t sVar1;
  
  sVar1 = write(__fd,__buf,__n);
  return sVar1;
}



/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int fclose(FILE *__stream)

{
  int iVar1;
  
  iVar1 = fclose(__stream);
  return iVar1;
}



/* WARNING: Unknown calling convention -- yet parameter storage is locked */

void setbuf(FILE *__stream,char *__buf)

{
  setbuf(__stream,__buf);
  return;
}



/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int printf(char *__format,...)

{
  int iVar1;
  
  iVar1 = printf(__format);
  return iVar1;
}



/* WARNING: Unknown calling convention -- yet parameter storage is locked */

ssize_t read(int __fd,void *__buf,size_t __nbytes)

{
  ssize_t sVar1;
  
  sVar1 = read(__fd,__buf,__nbytes);
  return sVar1;
}



/* WARNING: Unknown calling convention -- yet parameter storage is locked */

void srand(uint __seed)

{
  srand(__seed);
  return;
}



/* WARNING: Unknown calling convention -- yet parameter storage is locked */

char * fgets(char *__s,int __n,FILE *__stream)

{
  char *pcVar1;
  
  pcVar1 = fgets(__s,__n,__stream);
  return pcVar1;
}



/* WARNING: Unknown calling convention -- yet parameter storage is locked */

time_t time(time_t *__timer)

{
  time_t tVar1;
  
  tVar1 = time(__timer);
  return tVar1;
}



/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int tolower(int __c)

{
  int iVar1;
  
  iVar1 = tolower(__c);
  return iVar1;
}



/* WARNING: Unknown calling convention -- yet parameter storage is locked */

void * malloc(size_t __size)

{
  void *pvVar1;
  
  pvVar1 = malloc(__size);
  return pvVar1;
}



/* WARNING: Unknown calling convention -- yet parameter storage is locked */

FILE * fopen(char *__filename,char *__modes)

{
  FILE *pFVar1;
  
  pFVar1 = fopen(__filename,__modes);
  return pFVar1;
}



/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int atoi(char *__nptr)

{
  int iVar1;
  
  iVar1 = atoi(__nptr);
  return iVar1;
}



/* WARNING: Unknown calling convention -- yet parameter storage is locked */

size_t fwrite(void *__ptr,size_t __size,size_t __n,FILE *__s)

{
  size_t sVar1;
  
  sVar1 = fwrite(__ptr,__size,__n,__s);
  return sVar1;
}



/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int rand(void)

{
  int iVar1;
  
  iVar1 = rand();
  return iVar1;
}



/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int usleep(__useconds_t __useconds)

{
  int iVar1;
  
  iVar1 = usleep(__useconds);
  return iVar1;
}



void __cxa_finalize(void)

{
  __cxa_finalize();
  return;
}



void processEntry entry(undefined8 param_1,undefined8 param_2)

{
  undefined auStack_8 [8];
  
  __libc_start_main(main,param_2,&stack0x00000008,0,0,param_1,auStack_8);
  do {
                    /* WARNING: Do nothing block with infinite loop */
  } while( true );
}



/* WARNING: Removing unreachable block (ram,0x001011a3) */
/* WARNING: Removing unreachable block (ram,0x001011af) */

void FUN_00101190(void)

{
  return;
}



/* WARNING: Removing unreachable block (ram,0x001011e4) */
/* WARNING: Removing unreachable block (ram,0x001011f0) */

void FUN_001011c0(void)

{
  return;
}



void _FINI_0(void)

{
  if (DAT_00104038 != '\0') {
    return;
  }
  __cxa_finalize(PTR_LOOP_00104008);
  FUN_00101190();
  DAT_00104038 = 1;
  return;
}



void _INIT_0(void)

{
  FUN_001011c0();
  return;
}



void open_file(void)

{
  puts("Opening chonccfile...");
  file = fopen("/tmp/chonccfile","w");
  puts("Done");
  return;
}



void close_file(void)

{
  int iVar1;
  uint c;
  int i;
  
  puts("Closing chonccfile");
  if (file != (FILE *)0x0) {
    fclose(file);
  }
  for (i = 0; i < 0x1d0; i = i + 4) {
    iVar1 = rand();
    usleep(iVar1 % 100000);
    c = rand();
    *(uint *)((long)&file->_flags + (long)i) = c ^ *(uint *)((long)&file->_flags + (long)i);
  }
  puts("Done");
  return;
}



void write_file(void)

{
  int iVar1;
  time_t tVar2;
  char local_38 [40];
  size_t *i;
  
  tVar2 = time((time_t *)0x0);
  printf("Writing to chonccfile at timestamp %llu...\n",tVar2);
  puts("Are you sure you want to save? [Y/n]");
  fgets(local_38,0x10,stdin);
  iVar1 = tolower((int)local_38[0]);
  if (iVar1 == 0x6e) {
    puts("Writing chonccfile cancelled. Feel free to make more edits");
  }
  else {
    if (file == (FILE *)0x0) {
      puts("Chonccfile is not even opened. What are you doing, my friend?");
    }
    for (i = chunks; i != (size_t *)0x0; i = (size_t *)i[2]) {
      fwrite(i,4,1,file);
      fwrite((void *)i[1],*i,1,file);
    }
    puts("Done");
  }
  return;
}



void view_chunk(void)

{
  char local_22 [10];
  uint local_18;
  uint local_14;
  size_t *local_10;
  
  puts("Enter the choncc number:");
  fgets(local_22,10,stdin);
  local_18 = atoi(local_22);
  if ((int)local_18 < 1) {
    puts("huh");
  }
  else {
    local_10 = chunks;
    for (local_14 = 1; (local_10 != (size_t *)0x0 && (local_14 != local_18));
        local_14 = local_14 + 1) {
      local_10 = (size_t *)local_10[2];
    }
    if (local_10 == (size_t *)0x0) {
      puts("The choncc you wish to view does not exist.");
    }
    else {
      printf("%d: ",(ulong)local_18);
      write(1,(void *)local_10[1],*local_10);
      write(1,&DAT_00102171,1);
      puts("Done");
    }
  }
  return;
}



void edit_chunk(void)

{
  char local_22 [10];
  int idx;
  int i;
  size_t *local_10;
  
  puts("Enter the choncc number:");
  fgets(local_22,10,stdin);
  idx = atoi(local_22);
  if (idx < 1) {
    puts("huh");
  }
  else {
    local_10 = chunks;
    for (i = 1; (local_10 != (size_t *)0x0 && (i != idx)); i = i + 1) {
      local_10 = (size_t *)local_10[2];
    }
    if (local_10 == (size_t *)0x0) {
      puts("The choncc you wish to edit does not exist.");
    }
    else {
      puts("Enter the new content for the choncc:");
      read(0,(void *)local_10[1],*local_10);
      puts("Done");
    }
  }
  return;
}



/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void create_chunk(void)

{
  void *pvVar1;
  char local_2a [10];
  long *local_20;
  int size;
  long *i;
  
  puts("Enter the size of the choncc:");
  fgets(local_2a,10,stdin);
  size = atoi(local_2a);
  if (size < 1) {
    puts("huh");
  }
  else if (_MAX_SIZE < (ulong)(long)size) {
    puts("that\'s too much");
  }
  else {
    _MAX_SIZE = _MAX_SIZE - (long)size;
    local_20 = (long *)malloc(0x18);
    *local_20 = (long)size;
    pvVar1 = malloc((long)size);
    local_20[1] = (long)pvVar1;
    local_20[2] = 0;
    if (chunks == (long *)0x0) {
      chunks = local_20;
    }
    else {
      for (i = chunks; i[2] != 0; i = (long *)i[2]) {
      }
      i[2] = (long)local_20;
      puts("Done");
    }
  }
  return;
}



/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void remove_chunk(void)

{
  char local_2a [10];
  int idx;
  int i;
  long *local_18;
  long *local_10;
  
  if (chunks == (long *)0x0) {
    puts("You have no chonccs to remove");
  }
  else {
    puts("Enter the choncc number:");
    fgets(local_2a,10,stdin);
    idx = atoi(local_2a);
    if (idx < 1) {
      puts("huh");
    }
    else {
      local_10 = (long *)0x0;
      if ((chunks == (long *)0x0) || (idx != 1)) {
        local_18 = chunks;
        for (i = 2; (local_18[2] != 0 && (i != idx)); i = i + 1) {
          local_18 = (long *)local_18[2];
        }
        if ((i != idx) || (local_18[2] == 0)) {
          puts("The choncc you wish to remove does not exist.");
          return;
        }
        local_10 = (long *)local_18[2];
        local_18[2] = *(long *)(local_18[2] + 0x10);
      }
      else {
        local_10 = chunks;
        chunks = (long *)chunks[2];
      }
      _MAX_SIZE = _MAX_SIZE + *local_10;
      free((void *)local_10[1]);
      free(local_10);
      puts("Done");
    }
  }
  return;
}



void menu(void)

{
  puts("1. Create a choncc");
  puts("2. View a choncc");
  puts("3. Edit a choncc");
  puts("4. Remove a choncc");
  puts("5. Open  the chonccfile");
  puts("6. Close the chonccfile");
  puts("7. Write to the chonccfile");
  puts("8. Quit");
  printf("> ");
  return;
}



undefined8 main(void)

{
  time_t tVar1;
  char option [10];
  int local_10;
  int local_c;
  
  setbuf(stdout,(char *)0x0);
  setbuf(stdin,(char *)0x0);
  tVar1 = time((time_t *)0x0);
  srand((uint)tVar1);
  local_c = 1;
  while (local_c != 0) {
    menu();
    fgets(option,10,stdin);
    local_10 = atoi(option);
    switch(local_10) {
    default:
      puts("what options are you making up?");
      break;
    case 1:
      create_chunk();
      break;
    case 2:
      view_chunk();
      break;
    case 3:
      edit_chunk();
      break;
    case 4:
      remove_chunk();
      break;
    case 5:
      open_file();
      break;
    case 6:
      close_file();
      break;
    case 7:
      write_file();
      break;
    case 8:
      local_c = 0;
    }
  }
  return 0;
}



void _DT_FINI(void)

{
  return;
}



/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

void free(void *__ptr)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



/* WARNING: Control flow encountered bad instruction data */

void __libc_start_main(void)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



/* WARNING: Control flow encountered bad instruction data */

void _ITM_deregisterTMCloneTable(void)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int puts(char *__s)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

ssize_t write(int __fd,void *__buf,size_t __n)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int fclose(FILE *__stream)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

void setbuf(FILE *__stream,char *__buf)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int printf(char *__format,...)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

ssize_t read(int __fd,void *__buf,size_t __nbytes)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

void srand(uint __seed)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

char * fgets(char *__s,int __n,FILE *__stream)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



/* WARNING: Control flow encountered bad instruction data */

void __gmon_start__(void)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

time_t time(time_t *__timer)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int tolower(int __c)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

void * malloc(size_t __size)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

FILE * fopen(char *__filename,char *__modes)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int atoi(char *__nptr)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

size_t fwrite(void *__ptr,size_t __size,size_t __n,FILE *__s)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



/* WARNING: Control flow encountered bad instruction data */

void _ITM_registerTMCloneTable(void)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int rand(void)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Unknown calling convention -- yet parameter storage is locked */

int usleep(__useconds_t __useconds)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}



/* WARNING: Control flow encountered bad instruction data */

void __cxa_finalize(void)

{
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}

