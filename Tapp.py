# app.py
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from flask import Flask, session, redirect, url_for, request
from flask_ldap3_login import LDAP3LoginManager, AuthenticationResponseStatus
from auth import is_authenticated

# Flask server instance
server = Flask(__name__)
server.secret_key = 'super_secret_key'

# Dash app instance
app = dash.Dash(__name__, server=server)

# LDAP Configuration (example for LDAP, replace with actual config)
LDAP_HOST = 'ldap://your-ldap-server-url'
LDAP_BASE_DN = 'ou=users,dc=example,dc=com'

server.config['LDAP_HOST'] = LDAP_HOST
server.config['LDAP_BASE_DN'] = LDAP_BASE_DN
server.config['LDAP_USER_OBJECT_FILTER'] = '(sAMAccountName=%(username)s)'  # Active Directory example
server.config['LDAP_GROUP_MEMBERS_ATTR'] = 'member'
server.config['LDAP_GROUP_OBJECT_FILTER'] = '(objectclass=groupOfNames)'
server.config['LDAP_BIND_USER_DN'] = None  # If using anonymous bind
server.config['LDAP_BIND_USER_PASSWORD'] = None  # If using anonymous bind

ldap_manager = LDAP3LoginManager(server)

# Callback to handle successful LDAP login
@ldap_manager.save_user
def save_user(user_info, authentication):
    user = {
        'username': user_info['sAMAccountName'],
        'email': user_info['mail'],
        'name': user_info['displayName']
    }
    return user

# Define your main application layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

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
                <h2>Login Page</h2>
                <input type="text" name="username" placeholder="Username"/>
                <input type="password" name="password" placeholder="Password"/>
                <input type="submit" value="Login"/>
            </form>
        </body>
        </html>
    '''

# Logout route using Flask
@server.route('/logout')
def logout():
    session.pop('authenticated', None)
    session.pop('username', None)
    return redirect('/login')

# Middleware to check authentication before accessing the main app
@server.before_request
def before_request():
    if not is_authenticated() and request.endpoint not in ('login', 'static'):
        return redirect('/login')

# Callback to update page content based on URL
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    # This check is no longer needed since the middleware handles it
    if pathname == '/protected-page-1':
        return html.Div([html.H2(f'Hello, {session["username"]}'),
                         html.P('Content for protected page 1')])
    elif pathname == '/protected-page-2':
        return html.Div([html.H2(f'Hello, {session["username"]}'),
                         html.P('Content for protected page 2')])
    else:
        return html.Div([html.H2(f'Hello, {session["username"]}'),
                         html.P(f'Welcome to {pathname}')])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
