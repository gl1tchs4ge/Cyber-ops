# Brr

## Challenge Information

- **Platform:** TryHackMe
- **Room:** Brr
- **Category:** OT / SCADA
- **Difficulty:** Premium Room

## Objective

Assess the exposed OT environment, identify the SCADA interface, enumerate the connected PLC, and retrieve the hidden flag.

---

# Reconnaissance

To simplify interaction with the target, the hostname was added to the local hosts file.

    target.thm target

Connectivity was verified using ICMP.

    ping -c 1 target
    ping -c 1 target.thm

The host replied successfully with a TTL of 62, indicating the target was likely running a Linux-based operating system.

---

# Enumeration

A full TCP scan was performed.

    sudo nmap -sC -sV -sS -p- -T5 target -oM scan.md

## Open Ports

| Port | Service | Version |
|------|---------|---------|
| 22 | SSH | OpenSSH 9.6p1 Ubuntu |
| 80 | HTTP | WebSockify Python 3.12.3 |
| 5020 | Unknown (later identified as Modbus TCP) | zenginkyo-1? |
| 5901 | VNC | Protocol 3.8 |
| 8080 | HTTP | Apache Tomcat / Coyote JSP Engine 1.1 |

While the scan was running, visiting the HTTP service on port 80 returned:

    HTTP 405 Method Not Allowed

This confirmed an active web service but did not immediately expose useful functionality.

Accessing port 8080 revealed a SCADA BR login page powered by Mango M2M.

---

# Analysis

An authentication attempt using the default credentials succeeded.

**Username**

    admin

**Password**

    admin

This granted administrative access to the SCADA BR interface.

Within the authenticated dashboard, the **Data Sources** section contained a Modbus IP data source named:

    secret

Configuration:

| Property | Value |
|----------|-------|
| Name | secret |
| Type | Modbus IP |
| Host | plc |
| Port | 5020 |

This confirmed that port 5020 was not the service initially guessed by Nmap but was instead being used for Modbus communication with the PLC.

The associated point was:

| Property | Value |
|----------|-------|
| Point | test |
| Type | Binary |
| Slave ID | 1 |
| Offset | 0 |

After enabling the data source, the point began returning values, confirming successful communication between the SCADA server and the PLC.

---

# Exploitation

The `secret` Modbus data source was edited.

Within the **Modbus read data** section:

- Register Range was changed to **Holding Register**.
- Slave ID remained **1**.
- Offset remained **0**.
- The register values were read from the PLC.

The returned values were:

    54 48 4d 7b 6d 6f 64 62 75 73 5f 68 69 64 7d

These hexadecimal bytes were decoded using CyberChef.

**Recipe**

    From Hex

The decoded ASCII string produced the flag.

---

# Flag

The flag was successfully obtained.

    THM{modbus_hid}

---

# Lessons Learned

- Default credentials on industrial control systems can provide immediate administrative access.
- Service fingerprinting should always be validated through application-level enumeration. Although Nmap identified port 5020 as `zenginkyo-1?`, inspecting the SCADA configuration confirmed it was actually a Modbus TCP service.
- Administrative access to a SCADA interface may expose built-in tools for interacting directly with PLC registers.
- Modbus stores data in various register types (e.g., Coils, Discrete Inputs, Input Registers, and Holding Registers). Selecting the correct register type is essential for retrieving the intended data.
- Hexadecimal values transmitted by industrial protocols often represent ASCII strings or other encoded information and should be decoded during analysis.

---

# Key Takeaways

- Enumerate exposed services thoroughly before attempting exploitation.
- Validate automated scan results using information gathered from the application itself.
- Always test for default credentials when assessing administrative interfaces.
- Understand the underlying industrial protocol rather than relying solely on web application enumeration.
- Built-in diagnostic features within SCADA software can provide direct access to PLC data and may expose sensitive information if not properly secured.
