import folium
import geocoder
from auth import login
from models import User, Location
from app  import db
from flask import Blueprint, flash, render_template, request, redirect, url_for
from flask_login import current_user, login_required

views = Blueprint("views", __name__)

current_location=[]

@views.route("/")
@views.route("/home")
def home():
    current_location=geocoder.ip('me').latlng
    return render_template("home.html", user=current_user, location=current_location)

@views.route("/map")
@login_required
def show():
    return("Please allow access to location")

@views.route("/map/<lat>/<lng>")
@login_required
def show_map_loc(lat, lng):
    current_location = [lat, lng]
    f_map = folium.Map(location=current_location, zoom_start=14)
    locs = Location.query.all()
    for loc in locs:
        str=loc.user.number
        html =  f'''contact: {str}'''
        iframe = folium.IFrame(html,
                       width=90,
                       height=55)
        popup = folium.Popup(iframe,
                     max_width=200)

        folium.Marker(
        [loc.latitude, loc.longitude],
        popup=popup
        ).add_to(f_map)
    return f_map._repr_html_()

@views.route("/add-current-location")
@login_required
def show_error():
    return("Please allow access to location")

@views.route("/add-current-location/<lat>/<lng>")
@login_required
def add_curr_loc(lat, lng):

    f_map = folium.Map(location=[lat, lng], zoom_start=14)
    loc = Location(latitude = lat, longitude = lng, author=current_user.id)
    db.session.add(loc)
    db.session.commit()
    folium.Marker(
      location=[lat, lng]
    ).add_to(f_map)
    flash('Your current location has been added successfully', category="success")
    return f_map._repr_html_()

@views.route("/add-new-location", methods=['GET', 'POST'])
@login_required
def add_new_loc():
    if request.method=='POST':

        longitude = request.form.get("longitude")
        latitude = request.form.get('latitude')
        if not latitude or not longitude:
            flash("please enter valid location", category='error')
            return render_template("addlocation.html", user=current_user)
        loc = Location(latitude = latitude, longitude=longitude, author=current_user.id)
        db.session.add(loc)
        db.session.commit()
        flash('Your location has been added successfully', category="success")
        return redirect(url_for("views.home"))
    return render_template("addlocation.html", user=current_user)


@views.route("/<id>/locations")
@login_required
def show_locations(id):
    user = User.query.filter_by(id=id).first()
    locs = user.locations
    return render_template("locations.html", user=user, locs=locs)


@views.route("/<uid>/<lid>/remove-location")
@login_required
def remove_loc(uid, lid):
    loc = Location.query.filter_by(id=lid).first()
    if not loc:
        flash("location does not exists", category='error')
        return render_template("locations.html", user=user, locs=locs)
    db.session.delete(loc)
    db.session.commit()
    user = User.query.filter_by(id=uid).first()
    locs = user.locations
    flash("location successfully deleted!", category="success")
    return render_template("locations.html", user=user, locs=locs)
