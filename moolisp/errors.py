# -*- coding: utf-8 -*-

class LispError(Exception): 
    pass
class LispSyntaxError(SyntaxError, LispError): 
    pass
class LispNamingError(LookupError, LispError): 
    pass
class LispTypeError(TypeError, LispError): 
    pass
class LispPythonInteropError(LispError): 
    pass
