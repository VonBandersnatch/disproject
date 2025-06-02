from flask import Blueprint, render_template, request
from models.bills import list_bills, list_parties, party_vote


bp = Blueprint('bills', __name__, url_prefix='/')

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/bills', methods=['GET', 'POST'])
def bills():
    bills = []
    chosen_party = ''
    søgeord = ''
    vote = ''
    parties = list_parties()
    stemme = party_vote()
    if request.method == 'POST':
        chosen_party = request.form['choose_party']
        søgeord = request.form['searched_for']
        vote = request.form.get('party_vote','')
        bills = list_bills(chosen_party, søgeord, vote)
    return render_template('bills.html', bills=bills, parties=parties, chosen_party=chosen_party, søgeord=søgeord, vote=vote, stemme=stemme)
   