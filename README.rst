==============================
 Python visualizer on browser
==============================

It shows Python's bytecodes.

How to try
==========

-1 Run server: $ python server.py
-2 Enter '1 + 2' in textarea. Bytecodes are shown automatically.

TODO
====

- Better method to show the target of ABSOLUTE_JUMP, corresponding SETUP_LOOP and POP_BLOCK, etc.
- Nested function will shown as "LOAD_CONST <code object ...>". Should we support nexted functions?
- Show status such as 'compile error'.
- Link opname to document of those instruction http://docs.python.org/library/dis.html

