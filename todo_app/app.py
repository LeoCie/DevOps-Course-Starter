from flask import Flask, render_template, request
from werkzeug.utils import redirect
from todo_app.data.trello_items import get_items, create_item, delete_item, change_item_status
from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    items = get_items()
    items = sorted(items, key=lambda item: item.title)
    return render_template('index.html', items=items)

@app.route('/add', methods = ['POST'])
def addItem():
    title = request.form.get('title')
    create_item(title)
    return redirect('/')

@app.route('/delete', methods = ['POST'])
def deleteItem():
    item_id = request.form.get('item_id')
    delete_item(item_id)
    return redirect('/')

@app.route('/changeStatus', methods = ['POST'])
def changeItemStatus():
    item_id = request.form.get('item_id')
    new_status = request.form.get('status')
    change_item_status(item_id, new_status)
    return redirect('/')
