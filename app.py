"""
Main flask server functionality and logic.
"""
# pylint: disable=no-member
# pylint: disable=wrong-import-position
# pylint: disable=global-statement
import os
import logging
from os.path import join, dirname
from dotenv import load_dotenv
import flask
import flask_socketio
import flask_sqlalchemy
from google.oauth2 import id_token
from google.auth.transport import requests
from datetime import datetime

logging.getLogger("werkzeug").setLevel(logging.ERROR)

app = flask.Flask(__name__)

##BOILER PLATE CODE TO INITIATE SOCKETS
socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

dotenv_path = join(dirname(__file__), "sql.env")
load_dotenv(dotenv_path)

# BOILER PLATE CODE TO INSTANTIATE PSQL AND SQLALCHEMY

database_uri = os.environ["DATABASE_URL"]

app.config["SQLALCHEMY_DATABASE_URI"] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app)

db.init_app(app)
db.app = app


CALENDER_EVENT_CHANNEL = "calendar_event"

import models


def push_new_user_to_db(ident, name, email):
    """
    Pushes new user to database.
    """
    db.session.add(models.AuthUser(ident, name, email))
    db.session.commit()


def add_event(ccode, title, start, end, desc):
    """
    adds an event, returns id of added event
    """
    addedEvent = models.Event(ccode, title, start, end, desc)
    db.session.add(addedEvent)
    db.session.commit()
    return addedEvent.id
def mod_event(ccode, title, start, end, desc,event_id):
    """
    modifies an event, returns id of added event
    """
    event = db.session.query(models.Event).filter(models.Event.id==event_id).first()
    event.id = event_id
    event.title= title
    event.ccode = ccode
    event.start = start
    event.end = end
    event.desc = desc
    db.session.commit()
    emit_events_to_calender("recieve all events", ccode)


def add_calendar_for_user(userid, privFlag):

    """
    adds an event, returns the ccode of the new calendar
    """
    addedCalendar = models.Calendars(userid, privFlag)
    db.session.add(addedCalendar)
    db.session.commit()
    return addedCalendar.ccode


def get_sid():
    """
    returns sid.
    """
    sid = flask.request.sid
    return sid


def emit_events_to_calender(channel, cal_code):
    """
    Emits all calendar events along channel
    """
    sid = get_sid()
    all_events = []
    for ccode in [1, 2]:
        eventsForCcode = [
            {
                "start": record.start,
                "end": record.end,
                "title": record.title,
                "ccode": record.ccode,
                "eventid": record.id,
            }
            for record in db.session.query(models.Event)
            .filter(models.Event.ccode.contains([ccode]))
            .all()
        ]
        all_events.extend(eventsForCcode)

    for event in all_events:
        print(event)
    socketio.emit(channel, all_events, room=sid)


##SOCKET EVENTS
@socketio.on("connect")
def on_connect():
    """
    Runs on connect.
    """
    print("Someone connected!")


@socketio.on("disconnect")
def on_disconnect():
    """
    Runs on disconnect.
    """
    print("Someone disconnected!")


@socketio.on("new google user")
def on_new_google_user(data):
    """
    Runs verification on google token.
    """
    print("Beginning to authenticate data: ", data)
    sid = get_sid()
    try:
        idinfo = id_token.verify_oauth2_token(
            data["idtoken"],
            requests.Request(),
            "658056760445-ejq8q635n1948vqieqf95vsa6c6e1fvp.apps.googleusercontent.com",
        )
        userid = idinfo["sub"]
        print("Verified user. Proceeding to check database.")
        exists = (
            db.session.query(models.AuthUser.userid).filter_by(userid=userid).scalar()
            is not None
        )
        if not exists:
            push_new_user_to_db(userid, data["name"], data["email"])
            add_calendar_for_user(userid, False)
        all_ccodes = [
            record.ccode
            for record in db.session.query(models.Calendars)
            .filter_by(userid=userid)
            .all()
        ]
        socketio.emit(
            "Verified", {"name": data["name"], "ccodes": all_ccodes, "userid": userid}, room=sid
        )
        return userid
    except ValueError:
        # Invalid token
        print("Could not verify token.")
        return "Unverified."
    except KeyError:
        print("Malformed token.")
        return "Unverified."


@socketio.on("add calendar")
def on_add_calendar(data):
    """
    add a new calendar for user
    """
    print(data)
    userid = data["userid"]
    private = data["privateCal"]
    print(private)
    ccode = add_calendar_for_user(userid, private)
    print("Added calendar for user ", userid, "With ccode ", ccode, " Private flag: ", private)


@socketio.on("get events")
def send_events_to_calendar(data):
    print("LOOKING FOR CALCODE: ", data)
    emit_events_to_calender("recieve all events", data)
    print("SENT EVENTS!")


@socketio.on("new event")
def on_new_event(data):
    """
    add a new event for to calendar
    """
    print(data)
    title = data["title"]
    date = data["date"]
    start = data["start"]
    end = data["end"]
    ccode = data["ccode"]
    print(start)
    print(end)
    addedEventId = add_event([ccode], title, start, end, "some words")
    print("SENDING INDIVIDUAL EVENT")
    socketio.emit(
        "calender_event",
        {"title": title, "start": start, "end": end, "eventid": addedEventId, "ccode": [ccode]},
        room=get_sid(),
    )
    return addedEventId

@socketio.on("modify event")
def on_modify_event(data):
    """
    add a new event for to calendar
    """
    print(data)
    title = data["title"]
    date = data["date"]
    start = data["start"]
    end = data["end"]
    ccode = data["ccode"]
    event_id = data["event_id"]
    print(start)
    print(end)
    mod_event([ccode], title, start, end,"some words", event_id)


    
    
@socketio.on("cCodeToMerge")
def on_merge_calendar(data):
    merge_code = int(data["userToMergeWith"])
    print("LOOKING FOR CALCODE", data["userToMergeWith"])
    cal_code = int(data["currentUser"])
    checkExists = db.session.query(models.Calendars).filter_by(ccode=merge_code).first()
    print(checkExists)
    exists = (
        checkExists is not None and not checkExists.private
    )
    try:
        if not exists:
            raise ValueError
        for record in (
            db.session.query(models.Event)
            .filter(models.Event.ccode.contains([merge_code]))
            .all()
        ):
            if cal_code not in record.ccode:
                record.ccode.append(cal_code)
                db.session.commit()
            emit_events_to_calender("recieve all events", cal_code)
    except ValueError:
        print("Ccode does not exist, or you have attempted to merge with a private calendar.")


@app.route("/")
def hello():
    """
    Runs at page-load.
    
    """
    models.db.create_all()
    db.session.commit()
    print("User has joined.")
    return flask.render_template("index.html")


if __name__ == "__main__":
    socketio.run(
        app,
        host=os.getenv("IP", "0.0.0.0"),
        port=int(os.getenv("PORT", "8080")),
        debug=True,
    )