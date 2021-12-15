# from functools import wraps
# from flask import g, request, redirect, url_for

# from flask_httpauth import HTTPTokenAuth

# auth = HTTPTokenAuth(scheme='JWT')

# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if g.user is None:
#             return redirect(url_for('login', next=request.url))
#         return f(*args, **kwargs)
#     return decorated_function