from flask import render_template, request, Blueprint
from skillnecting.models import Post

debugme = Blueprint('debugme', __name__)


@debugme.route("/debugme", methods=['GET', 'POST'])
def debug_me():
    return render_template('debugme.html', title='Debug me')

