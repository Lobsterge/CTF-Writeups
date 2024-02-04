# toll_bridge [rev]

### Challenge:
Toll Bridge: 
Pay the toll and cross the bridge.

##### Links: ```nc chal.bearcatctf.io 32610```
##### Files: [challenge.zip](challenge.zip)

### Solution:

We had to make either the bribe or toll functions return true to get the flag, 
i've only analyzed the bribe function because it seemed easier.

```c
bool bribe(char *param_1)
{
  bool bVar1;
  
  if ((int)param_1[2] + (int)param_1[1] == 0) {
    bVar1 = false;
  }
  else if (((*param_1 == '\0') || (param_1[1] == '\0')) || (param_1[2] == '\0')) {
    bVar1 = false;
  }
  else {
    bVar1 = (int)param_1[2] + ((int)*param_1 - (int)param_1[1]) == 0x30;
  }
  return bVar1;
}
```

Long story short we need to make this condition evaluate to true:

```c
(int)param_1[2] + ((int)*param_1 - (int)param_1[1]) == 0x30;
```

We can achieve that by using the input 000, which whill sum 0x30 and 0, giving us our flag. 

Flag: ```BCCTF{GoTta_PaY_Th4t_tR01L_t0L1_1c0457c5}```