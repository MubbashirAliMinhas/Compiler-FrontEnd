class RedeclarationError(NameError):
    pass

class UndeclaredError(NameError):
    pass

class DuplicationError(NameError):
    pass

class ConstantError(ValueError):
    pass

class OverridingError(LookupError):
    pass

class ObjectCreationError(TypeError):
    pass

class AccessError(NameError):
    pass

class ReturnTypeError(TypeError):
    pass