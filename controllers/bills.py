from flask import Blueprint, render_template, request
from models.bills import list_bills, list_parties


bp = Blueprint('bills', __name__, url_prefix='/')

@bp.route('/bills', methods=['GET', 'POST'])
def bills():
    bills = []
    chosen_party = ''
    søgeord = ''
    parties = list_parties()
    if request.method == 'POST':
        chosen_party = request.form['choose_party']
        søgeord = request.form['searched_for']
        bills = list_bills(chosen_party, søgeord)
    return render_template('bills.html', bills=bills, parties=parties, chosen_party=chosen_party, søgeord=søgeord)

