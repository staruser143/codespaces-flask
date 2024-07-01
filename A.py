# app.py
import dash
from dash import dcc, html, Input, Output
from flask import Flask, session, redirect, request
from flask_ldap3_login import LDAP3LoginManager, AuthenticationResponseStatus
import dash_bootstrap_components as dbc
from auth import is_authenticated
from login import login  # Import the login route

# Flask server instance
server = Flask(__name__)
server.secret_key = 'super_secret_key'

# Dash app instance
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])

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
