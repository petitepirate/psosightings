from flask import Flask, render_template, request, flash, redirect, session, g, abort
from models import db, connect_db, User, Sighting
from forms import NewUserForm, LoginForm, AddSightingForm, EditUserForm, EditSightingForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc
import os
import requests
import pdb
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

CURR_USER_KEY = "curr_user"

app = Flask(__name__)
app.config.from_object(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'postgresql:///psosightings')
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', '12345678')


connect_db(app)
db.create_all()
# toolbar = DebugToolbarExtension(app)


#### USERS ROUTES #####
@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id

def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route("/user/new", methods=["GET"])
def users_new_form():
    """Show a form to create a new user"""
    
    form= NewUserForm()

    return render_template('new_user.html', form=form)

@app.route("/user/new", methods=["POST"])
def add_user():

    form = NewUserForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                user_name=form.user_name.data,
                email=form.email.data,
                password=form.password.data
                )   

            # db.session.add(user)
            # session["user_id"] = user.id

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('new_user.html', form=form)


        return redirect(f"/user/{user.id}")  ## CHANGE TO ADMIN ID NUMBER


    else:
        return render_template('new_user.html', form=form)

    return redirect('/home')
    # return redirect('/user/info/<int:user_id>')

@app.route('/user/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.user_name.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.user_name}!", "success")

            return redirect(f"/user/{user.id}")

        flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()
    flash("Goodbye for now!", "success")
    return redirect("/")



@app.route("/user/<int:user_id>", methods=["GET"])
def user_page(user_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/user/<int:user_id>")

    user = User.query.get_or_404(user_id)
    sightings = Sighting.query.filter(Sighting.user_id == user_id).all()

    return render_template('user_info.html', user=user, sightings=sightings)    


@app.route("/user/<int:user_id>/edit")
def edit_user(user_id):
    """Show edit form"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/user/<int:user_id>")

    user = User.query.get(g.user.id)
    form = EditUserForm(obj=user)

    return render_template("edit_user.html", user=user, form=form)


@app.route('/user/<int:user_id>/edit', methods=["POST"])
def submit_edit(user_id):
    """Edit a user"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/user/<int:user_id>")
        
    user = User.query.get_or_404(user_id)
    user_name=request.form["user_name"]
    email=request.form["email"]

    db.session.add(user)
    db.session.commit()

    return redirect(f"/user/{user.id}")


@app.route('/user/delete', methods=["POST"])
def delete_user():
    """Delete user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/user/<int:user_id>")

    do_logout()

    db.session.delete(g.user)
    db.session.commit()

    return redirect("/")

#### HOME ROUTES ####
@app.route("/user/<int:user_id>/all")
def enterpage(user_id):

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/user/<int:user_id>")

    sightings = Sighting.query.order_by(Sighting.id.desc()).all()[::]
    # Sighting.query.all.(order_by(desc(Sighting.id)))  
    user = User.query.get_or_404(user_id) 
    return render_template('list.html', sightings=sightings, user=user)

@app.route("/")
def homepage():


    return redirect("/user/login")

@app.route("/user/<int:user_id>/addsighting", methods=["GET"])
def new_sighting(user_id):

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/user/<int:user_id>")

    user = User.query.get_or_404(user_id)
    form = AddSightingForm()

    return render_template('new_sighting.html', user=user, form=form)

@app.route("/user/<int:user_id>/addsighting", methods=["POST"])
def submit_sighting(user_id):

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/user/<int:user_id>")
    TO_EMAILS= [('msmeganmcmanus@gmail.com', 'Megan McManus'), ('psosharespace@gmail.com', 'Megan McManus2'), ('neilroper15@gmail.com', 'Neil Roper'), ('katiedouglas11@gmail.com', 'Katie Douglas')]
    user = User.query.get_or_404(user_id)
    form = AddSightingForm()

    if form.validate_on_submit():
        sighting_num = form.sighting_num.data
        date = form.date.data
        time = form.time.data
        latitude = form.latitude.data
        longitude = form.longitude.data
        species = form.species.data
        individuals = form.individuals.data
        user_id = f"{user.id}"

        sighting= Sighting(sighting_num=sighting_num, date=date, time=time, latitude=latitude, longitude=longitude, species=species, individuals=individuals, user_id=user_id)

        db.session.add(sighting)
        db.session.commit()

        message = Mail(
        from_email='psosharespace@gmail.com',
        to_emails=TO_EMAILS,
        is_multiple=True, 
        subject=f"New Sighting Submitted by {sighting.user.user_name}",
        html_content=f"At {sighting.time}, {sighting.user.user_name} observed a {sighting.species} at {sighting.latitude}N, {sighting.longitude}W - Date {sighting.date}")
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)

        return redirect(f"/user/{user.id}/all")
    
    return render_template('new_sighting.html', form=form, user=user)

@app.route("/sighting/<int:sighting_id>/editsighting", methods=["GET"])
def edit_sighting(sighting_id):
    """Show edit form"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/user/<int:user_id>")

    sighting = Sighting.query.get_or_404(sighting_id)
    form = EditSightingForm(obj=sighting)
    user = User.query.get_or_404(g.user.id)
    return render_template("edit_sighting.html", user=user, sighting=sighting, form=form)

@app.route("/sighting/<int:sighting_id>/editsighting", methods=["POST"])
def submit_edit_sighting(sighting_id):

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/user/<int:user_id>")

    sighting = Sighting.query.get_or_404(sighting_id)
    form = EditSightingForm(obj=sighting)
    user = User.query.get_or_404(g.user.id)

    if form.validate_on_submit():
        sighting.sighting_num = form.sighting_num.data
        sighting.date = form.date.data
        sighting.time = form.time.data
        sighting.latitude = form.latitude.data
        sighting.longitude = form.longitude.data
        sighting.species = form.species.data
        sighting.individuals = form.individuals.data
        user_id = f"{user.id}"

        sighting= Sighting(sighting_num=sighting.sighting_num, date=sighting.date, time=sighting.time, latitude=sighting.latitude, longitude=sighting.longitude, species=sighting.species, individuals=sighting.individuals, user_id=user_id)


        db.session.commit()

        return redirect(f"/user/{user.id}/all")



@app.route('/sighting/<int:sighting_id>/delete', methods=["POST"])
def submit_job_edit(sighting_id):

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/user/<int:user_id>")

    sighting = Sighting.query.get_or_404(sighting_id)
    if sighting.user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect(f"/user/{g.user.id}")

    db.session.delete(sighting)
    db.session.commit()

    return redirect(f"/user/{g.user.id}")



@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req

if __name__ == '__main__':
    app.run(debug=True)
