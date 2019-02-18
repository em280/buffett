"""
@author: EM
"""

from flask import redirect 
from functools import wraps

def usd(value):
    """
    @author: EM
    Format an amount in usd currency.
    """
    return f"${value:,.2f}"

def loginRequire(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        """
        @author: SA
        Login is required to progress to next page. 
        """
        return redirect("/login")
    return decorated_function