from flask import Flask, render_template, request
from flask_login import LoginManager, current_user, login_required, login_user
import os
import requests
from werkzeug.utils import redirect
from todo_app.data.mongodb_items import get_items, create_item, delete_item, change_item_status
from todo_app.flask_config import Config
from todo_app.models.User import User
from todo_app.models.ViewModel import ViewModel
from functools import wraps
from flask import abort

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    login_manager = LoginManager()
    app.config['LOGIN_DISABLED'] = os.getenv('LOGIN_DISABLED') == 'True'

    auth_mapping = {"78739678": "writer"}

    def user_in_group(current_user, group):
        if(app.config.get('LOGIN_DISABLED') == True):
            return True
        if current_user is None or not current_user.is_authenticated:
            return False
        if auth_mapping[current_user.get_id()] != group:
            return False
        return True

    def writer_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not user_in_group(current_user, "writer"):
                abort(404)
            return f(*args, **kwargs)
        return decorated_function

    def reader_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not user_in_group(current_user, "reader") and not user_in_group(current_user, "writer"):
                abort(404)
            return f(*args, **kwargs)
        return decorated_function

    @login_manager.unauthorized_handler
    def unauthenticated():
        client_id = os.getenv('GITHUB_CLIENT_ID')
        return redirect(f'https://github.com/login/oauth/authorize?client_id={client_id}', code=302)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id)

    login_manager.init_app(app)

    @app.route('/login/callback')
    def login():
        client_id = os.getenv('GITHUB_CLIENT_ID')
        client_secret = os.getenv('GITHUB_CLIENT_SECRET')
        access_request = requests.post("https://github.com/login/oauth/access_token",
            [("client_id", client_id), ("client_secret", client_secret), ("code", request.args.get("code"))],
            headers={"Accept": "application/json"})
        access_code = access_request.json()["access_token"]
        github_user = requests.get("https://api.github.com/user", headers={"Accept": "application/vnd.github+json", "Authorization": f"Bearer {access_code}"})
        user = User(github_user.json()['id'])
        login_user(user)
        return redirect("/")

    @app.route('/')
    @reader_required
    @login_required
    def index():
        items = get_items()
        items = sorted(items, key=lambda item: item.created)
        item_view_model = ViewModel(items)
        return render_template('index.html', view_model=item_view_model, show_actions = user_in_group(current_user, "writer"))

    @app.route('/add', methods = ['POST'])
    @writer_required
    @login_required
    def addItem():
        title = request.form.get('title')
        create_item(title)
        return redirect('/')

    @app.route('/delete', methods = ['POST'])
    @writer_required
    @login_required
    def deleteItem():
        item_id = request.form.get('item_id')
        delete_item(item_id)
        return redirect('/')

    @app.route('/changeStatus', methods = ['POST'])
    @writer_required
    @login_required
    def changeItemStatus():
        item_id = request.form.get('item_id')
        new_status = request.form.get('status')
        change_item_status(item_id, new_status)
        return redirect('/')

    return app
