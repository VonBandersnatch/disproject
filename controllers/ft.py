from flask import Blueprint, render_template, request
from models.ft import list_bills
from models.ft import list_parties

bp = Blueprint('ft', __name__, url_prefix='/')
partylist = list_parties()
@bp.route('/ft', methods=['GET','POST'])


def index():

    if request.method == 'POST':
        search_text = request.form.get('search_text', '').strip()
        selected_party = request.form.get('dropdown_option', '')
        print(search_text, selected_party)
        bills = list_bills(selected_party, search_text)
    else:
        bills = []
    return render_template(
        'ft.html',
        #dropdown_options=[('V','V'),('EL', 'EL')],
        dropdown_options = partylist,
        bills = bills
        )

def bills():
    # bills = list_bills(selected_party, search_text)
    return render_template('ft.html',bills=bills, dropdown_options=partylist)
