# login.py
from flask import session, redirect, request
from app import server, ldap_manager  # Import server and ldap_manager from your main app file
from flask_ldap3_login import AuthenticationResponseStatus

# Login route using Flask
@server.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':  # When the form is submitted
        username = request.form['username']
        password = request.form['password']

        # Authenticate the user with LDAP
        response = ldap_manager.authenticate(username, password)

        if response.status == AuthenticationResponseStatus.success:
            # On successful authentication
            session['authenticated'] = True
            session['username'] = username
            return redirect('/')  # Redirect to the main page of the Dash app
        else:
            # On authentication failure
            return 'Authentication failed. Please check your credentials.'

    # When the user first accesses the login page (HTTP GET method)
    return '''
        <!DOCTYPE html>
        <html>
        <head>
            <link rel="stylesheet" type="text/css" href="/static/styles.css">
        </head>
        <body>
            <form class="login-form" method="post">
                <h2 class="text-center">Login Page</h2>
                <div class="form-group">
                    <label for="username">Username</label>
                    <input type="text" name="username" class="form-control" placeholder="Username"/>
                </div>
                <div class="form-group">
                    <label for="password">Password</label>
                    <input type="password" name="password" class="form-control" placeholder="Password"/>
                </div>
                <button type="submit" class="btn btn-primary btn-block">Login</button>
            </form>
        </body>
        </html>
    '''
