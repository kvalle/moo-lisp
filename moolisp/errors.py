# -*- coding: utf-8 -*-

class LispError(Exception): 
    pass
class LispSyntaxError(SyntaxError, LispError): 
    pass
class LispNamingError(LookupError, LispError): 
    pass
