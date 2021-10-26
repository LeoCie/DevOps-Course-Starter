from flask import Flask, render_template, request
from werkzeug.utils import redirect
from todo_app.data.session_items import add_item, delete_item, get_item, get_items, save_item

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    items = get_items()
    items = sorted(items, key=lambda item: item['status'])
    return render_template('index.html', items=items)

@app.route('/add', methods = ['POST'])
def addItem():
    title = request.form.get('title')
    add_item(title)
    return redirect('/')

@app.route('/delete', methods = ['POST'])
def deleteItem():
    item_id = request.form.get('item_id')
    delete_item(item_id)
    return redirect('/')

@app.route('/markComplete', methods = ['POST'])
def markItemAsComplete():
    item_id = request.form.get('item_id')
    item = get_item(item_id)
    item['status'] = 'Completed'
    save_item(item)
    return redirect('/')
