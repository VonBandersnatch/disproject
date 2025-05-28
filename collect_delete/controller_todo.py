from flask import Blueprint, render_template, request
from models.todo import list_todos, insert_todo
from models.category import list_categories
from models.bills import list_parties, list_bills

bp = Blueprint('todo', __name__, url_prefix='/')

@bp.route('/todo', methods=['GET', 'POST'])
def todos():
    bills = []
    valgt_parti = ""
    
    if request.method == 'POST':
        todo_text = request.form['new_todo']
        category_id = request.form['category_todo']
        insert_todo(todo_text, category_id)
        valgt_parti = request.form['chosen_party']
        bills = list_bills(valgt_parti)

    categories = list_categories()

    todos = list_todos()

    parties = list_parties()

    return render_template('todo.html', todos=todos, categories=categories, parties=parties, text1="Nice summer", bills=bills, valgt_parti=valgt_parti)
