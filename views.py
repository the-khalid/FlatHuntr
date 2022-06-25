from flask_googlemaps import Map
import geocoder
from app import db, User, Location
from auth import login
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
    n="heyaa"
    gmap = Map(
        identifier="view-side",
        lat=18.0118336,
        lng=79.5788428,
        style="height:600px;width:600px;margin:20;",
        streetview_control=1,
        scroll_wheel=1,
        markers=[
            {
                'lat':18.0118336,
                'lng':79.5788428,
                'infobox':n
            }
        ]
    )
    return render_template('map.html', gmap=gmap)

@views.route("/map/<lat>/<lng>")
@login_required
def show_map_loc(lat, lng):
    current_location = [lat, lng]
    locs = Location.query.all()
    num_of_locs=len(locs)
    if(len(locs)!=0):
        gmap = Map(
            identifier="view-side",
            lat=float(lat),
            lng=float(lng),
            zoom=14,
            center_on_user_location=1,
            style="height:600px;width:400px;margin:40;",
            streetview_control=1,
            scroll_wheel=1,
            markers=[(float(loc.latitude), float(loc.longitude), str("contact: "+loc.user.number)) for loc in locs]
        )
        return render_template("map.html", gmap=gmap, user=current_user, stat=num_of_locs)
    else:
        flash("There are zero flats available right now :(")
    return render_template("home.html", user=current_user, location=current_location)

@views.route("/add-current-location")
@login_required
def show_error():
    return("Please allow access to location")

@views.route("/add-current-location/<lat>/<lng>")
@login_required
def add_curr_loc(lat, lng):
    loc = Location(latitude = lat, longitude = lng, author=current_user.id)
    db.session.add(loc)
    db.session.commit()
    flash('Your current location has been added successfully', category="success")
    return redirect(url_for("views.home"))


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
    return render_template("locations.html", user=current_user, locs=locs)


@views.route("/<uid>/<lid>/remove-location")
@login_required
def remove_loc(uid, lid):
    loc = Location.query.filter_by(id=lid).first()
    if not loc:
        flash("location does not exists", category='error')
        return render_template("locations.html", user=current_user, locs=locs)
    db.session.delete(loc)
    db.session.commit()
    user = User.query.filter_by(id=uid).first()
    locs = user.locations
    flash("location successfully deleted!", category="success")
    return render_template("locations.html", user=user, locs=locs)
