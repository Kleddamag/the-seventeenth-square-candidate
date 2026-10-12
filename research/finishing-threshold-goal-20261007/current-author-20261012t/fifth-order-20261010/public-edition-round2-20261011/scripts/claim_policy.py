"""Finite editorial policy: spacing and one explicit strict-contraction correction."""
import re
from fractions import Fraction
SPACING=('all','below','label','region','regions','role','is','satisfies','dated','atom')
def corrected(identifier,text):
    if identifier=='G20S_PHYSICAL':
        assert text.count('ratio below0.796')==1
        assert Fraction(159201934153319,200000000000000)>Fraction(796,1000)
        assert Fraction(159201934153319,200000000000000)<1
        text=text.replace('ratio below0.796','ratio 159201934153319/200000000000000 < 1')
    text=re.sub(r'\b('+ '|'.join(SPACING)+r')(?=[0-9])',r'\1 ',text)
    text=text.replace('the18:38 notes','the cited notes')
    return text
