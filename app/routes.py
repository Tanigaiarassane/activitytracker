
from app import app
from app.models import User
from app.models import ActivityItem, Mathematician
from app import db
from flask import render_template,flash, redirect, url_for,request
from app.forms import ToDO, SignInForm, LoginForm
from app import bcrypt
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
def base():
    return render_template("base.html")

@app.route("/sample")
def sample():
    return render_template("sample.html", greetings="Hello sir", title="Sample")

@app.route("/todo/list")
@login_required
def listing():
    print "current user {}".format(current_user)
    todo = ActivityItem.query.all()
    return render_template("listing.html", todo=todo, title="Item litem")

@app.route("/todo/create", methods = ['GET', 'POST'])
@login_required
def create():
    form = ToDO()
    if form.validate_on_submit():
        print "welcome"
        print "Submitted values - {} -  {} - {}".format(form.name.data, form.content.data, form.status.data)
        activity = ActivityItem(name=form.name.data, content=form.content.data,status=form.status.data,user_id = current_user.id)
        db.session.add(activity)
        db.session.commit()
        message = "Successfully created an activity - {}".format(activity.name)
        flash(message, "success")
        return redirect( url_for('item', item_id=activity.id) )
    print "outside"
    return render_template("create.html",  message="Create item", form=form)

@app.route("/todo/curr_user_list", methods = ["POST","GET"])
@login_required
def curruser_list():
    user = User.query.filter_by(id=current_user.id).first()
    print user
    print "id {} ".format(current_user.email)
    if user:
        todo = user.todo_list
        return render_template("listing.html", todo=todo, title="Item List")


@app.route("/todo/item/<int:item_id>", methods = ["POST","GET"])
def item(item_id):
    print item_id
    todo = ActivityItem.query.get_or_404(item_id)
    return render_template('list.html', todo = todo)

@app.route("/todo/<int:todo_id>/update", methods = ["POST","GET"])
def update(todo_id):
    todo = ActivityItem.query.get_or_404(todo_id)
    form = ToDO()
    print "todo id - {} ; current use"
    if todo.user_id != current_user.id:
        msg = "You do not have permission to update this list"
        flash(msg, "failure")
        return redirect(url_for('listing'))
    if form.validate_on_submit():
        todo.name = form.name.data
        todo.content = form.content.data
        todo.status = form.status.data
        db.session.commit()
        message = "Successfully updated activity to- {}".format(todo.name)
        flash(message,"success")
        return redirect(url_for('listing'))
    elif request.method == "GET":
        form.name.data = todo.name
        form.content.data = todo.content
        form.status.data = todo.status
    return render_template("create.html",  message="Update item", form=form)

@app.route("/todo/<int:todo_id>/delete", methods = ["POST","GET"])
def delete(todo_id):
    todo = ActivityItem.query.get_or_404(todo_id)
    message = "Successfully deleted activity - {}".format(todo.name)
    db.session.delete(todo)
    db.session.commit()
    flash(message, "success")
    return redirect(url_for('listing'))

@app.route("/signin", methods=["POST", "GET"])
def signin():
    form = SignInForm()
    if form.validate_on_submit():
        e_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, email=form.email.data, password=e_password)
        db.session.add(user)
        db.session.commit()
        msg = "Created user {}".format(form.name.data)
        flash(msg,"success")
    return render_template("SignInForm.html", form=form)


@app.route("/login", methods = ["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember=form.remember.data)
            msg = "Logged in {}".format(current_user.id)
            flash(msg,"success")
            return redirect(url_for('listing'))
    return render_template("LoginForm.html", form = form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('sample'))

############################ Webscrapping services #####################
@app.route('/topN')
def topNmaths():
    math_list = Mathematician.query.order_by(Mathematician.hit.desc()).limit(10).all()
    return render_template("mathlist.html", todo=math_list, title="Item litem")



