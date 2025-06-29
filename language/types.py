# --- language/types.py ---
class ELANType:
    def __init__(self, typename):
        self.typename = typename

    def __str__(self):
        return self.typename

    def __eq__(self, other):
        return isinstance(other, ELANType) and self.typename == other.typename


# Primitive types
Number = ELANType('Number')
Vector = ELANType('Vector')
Complex = ELANType('Complex')
String = ELANType('String')
Boolean = ELANType('Boolean')
Function = ELANType('Function')
