# main.py
import datetime

from .docker_manager import run_container
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
        select = request.form.get('conteiner_btn')
        print(select)

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


    # if request.method == 'POST':
    #     if 'conteiner_btn' in request.form:
    #         print(request.form['conteiner_btn'])
    #     elif 'create_btn' in request.form:
    #         print(request.form['create_btn'])
    #     elif 'stop_btn' in request.form:
    #         print(request.form['stop_btn'])
    #     elif 'delete_btn' in request.form:
    #         print(request.form['delete_btn'])
    #     else:
    #         pass  # unknown
    # elif request.method == 'GET':
    #     # return render_template("index.html")
    #     print("No Post Back Call")

    info = []
    try:
        info = Conteiners.query.all()
    except:
        print("Error")

    name = current_user.name
    return render_template('profile.html', name=name, list=info)
