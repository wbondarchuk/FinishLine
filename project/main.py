# main.py
import datetime

from .docker_manager import run_container, force_remove_container, get_URL
from flask import Blueprint, render_template, request, session, abort, current_app
from flask_login import current_user, login_required
from . import db
from .models import Users, Conteiners

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        data = request.form.getlist('chkbox')
        print(data)

        if 'create_btn' in request.form:
            print(request.form['create_btn'])
            (host, port, container) = run_container()
            print(current_user.id)
            print(container)
            new_container = Conteiners(id=container, user_id=current_user.id)

            # add the new container to the database
            db.session.add(new_container)
            db.session.commit()

            return render_template('loader.html'), {"Refresh": f"5; url=http://{host}:{port}"}

        elif 'delete_btn' in request.form:
            print(request.form['delete_btn'])
            for id in data:
                print(id)
                force_remove_container(id)

        elif 'share_btn' in request.form:
            print(request.form['share_btn'])
            for id in data:
                print(id)
                URL = get_URL(id)




    info = []
    try:
        info = Conteiners.query.all()
    except:
        print("Error")

    name = current_user.name
    return render_template('profile.html', name=name, list=info)
