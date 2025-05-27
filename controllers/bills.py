from flask import Blueprint, render_template, request
from models.bills import list_bills

bp = Blueprint('bills', __name__, url_prefix='/')

@bp.route('/bills', methods=['GET'])
def bills():
    bills = list_bills()
    return render_template('bills.html',bills=bills)

