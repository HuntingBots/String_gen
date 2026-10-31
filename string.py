#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MIT License

Copyright (c) 19-10-2026 @HuntingBots for MatrixVcBot

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

"""
Compatibility shim for string.py
If imported as standard library 'string', delegates to python stdlib 'string'.
If run directly, executes the String Session Generator.
Author: @HuntingBots for MatrixVcBot
"""

import sys
import os

if __name__ != "__main__":
    import importlib.machinery
    import importlib.util
    _cur_dir = os.path.dirname(os.path.abspath(__file__))
    _stdlib_paths = [p for p in sys.path if p and os.path.abspath(p) != _cur_dir]
    _spec = importlib.machinery.PathFinder.find_spec("string", _stdlib_paths)
    if _spec and _spec.loader:
        _real_string = importlib.util.module_from_spec(_spec)
        _spec.loader.exec_module(_real_string)
        sys.modules["string"] = _real_string
        globals().update(_real_string.__dict__)
else:
    from generate import main
    main()
