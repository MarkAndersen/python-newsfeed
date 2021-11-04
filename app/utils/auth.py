from flask import session, redirect
from functools import wraps

def login_required(func):
    # wraps(func) preserves callback functions original name.
    @wraps(func)
    # *args and **kwargs preserve all of the passed in args given to the wrapped callback function
    def wrapped_function(*args, **kwargs):
        #if logged in, call original function with original arguments
        if session.get('loggedIn') == True:
            return func(*args, **kwargs)
        return redirect('/login')   
    return wrapped_function

