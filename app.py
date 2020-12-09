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
import iso8601
from oauth2client import client
from googleapiclient.discovery import build

API_NAME = "calendar"
API_VERSION = "v3"
CLIENT_SECRET_FILE = "./credentials.json"
from iteration_utilities import unique_everseen

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


def mod_event(ccode, title, start, end, desc, event_id):
    """
    modifies an event, returns id of added event
    """
    event = db.session.query(models.Event).filter(models.Event.id == event_id).first()
    event.id = event_id
    event.title = title
    event.ccode = ccode
    event.start = start
    event.end = end
    event.desc = desc
    db.session.commit()
    emit_events_to_calender("recieve all events", ccode)


def del_event(event_id, ccode):
    """
    Deletes an event and returns the id of the deleted event.
    """
    db.session.query(models.Event).filter(models.Event.id == event_id).delete()
    db.session.commit()


def delete_cal(ccode):
    print("Deleting all events!")
    print(":GOT HERE GOT HERE GOT HERE GOT HERE")
    for record in (
        db.session.query(models.Event).filter(models.Event.ccode.contains(ccode)).all()
    ):
        print(record)
    db.session.query(models.Calendars).filter(models.Calendars.ccode == ccode).delete()
    db.session.commit()


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
    return flask.request.sid


def emit_events_to_calender(channel, cal_code):
    """
    Emits all calendar events along channel
    """
    sid = get_sid()
    all_events = []
    for ccode in cal_code:
        events_for_ccode = [
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
        all_events.extend(events_for_ccode)

    all_events = list(unique_everseen(all_events))
    # for event in all_events:
    #     print(event)
    socketio.emit(channel, all_events, room=sid)


def rfc3339_to_unix(timestamp):
    """
    Convert to unix time.
    """
    _date_obj = iso8601.parse_date(timestamp)
    _date_unix = _date_obj.timestamp()
    return _date_unix


def emit_ccode_to_calender(channel, ccodes):
    """
    emits details about a ccode
    """
    sid = get_sid()
    ccode_details = {}
    for ccode in ccodes:
        record = (
            db.session.query(models.Calendars)
            .filter(models.Calendars.ccode == ccode)
            .first()
        )
        details_for_ccode = {
            "userid": record.userid,
            "private": record.private,
        }
        ccode_details[record.ccode] = details_for_ccode

    if len(ccode_details) > 0:
        socketio.emit(channel, ccode_details, room=sid)


def exists_in_auth_user(check_id):
    """
    Check to see if the auth user is there
    """
    return (
        db.session.query(models.AuthUser.userid).filter_by(userid=check_id).scalar()
        is not None
    )


def exists_in_calender(merge_code):
    """
    Check to see if merge calendar exists
    """
    return (
        db.session.query(models.Calendars.ccode).filter_by(ccode=merge_code).scalar()
        is not None
    )


##SOCKET EVENTS
@socketio.on("connect")
def on_connect():
    """
    Runs on connect.
    """
    # print("Someone connected!")


@socketio.on("disconnect")
def on_disconnect():
    """
    Runs on disconnect.
    """
    # print("Someone disconnected!")


@socketio.on("new google user")
def on_new_google_user(data):
    """
    Runs verification on google token.
    """
    print("Beginning to authenticate data: ", data)
    sid = get_sid()
    try:
        credentials = client.credentials_from_clientsecrets_and_code(
            CLIENT_SECRET_FILE,
            ["https://www.googleapis.com/auth/calendar.readonly", "profile", "email"],
            data["code"],
        )
        print("Verified user. Proceeding to check database.")
        userid = credentials.id_token["sub"]
        email = credentials.id_token["email"]
        name = credentials.id_token["name"]
        exists = exists_in_auth_user(userid)
        if not exists:
            push_new_user_to_db(userid, name, email)
            add_calendar_for_user(userid, False)
        all_ccodes = [
            record.ccode
            for record in db.session.query(models.Calendars)
            .filter_by(userid=userid)
            .all()
        ]
        socketio.emit(
            "Verified",
            {
                "name": name,
                "ccodes": all_ccodes,
                "userid": userid,
                "access_token": credentials.access_token,
            },
            room=sid,
        )
        #
        # print("printing all CCODES")
        # print(all_ccodes)
        #
        return userid
    except ValueError:
        # Invalid token
        print("Could not verify token.")
        return "Unverified."
    except KeyError:
        print("Malformed token.")
        return "Unverified."


@socketio.on("delete calendar")
def on_delete_cal(data):
    """
    add a new event for to calendar
    """
    print("not updating?")
    delete_cal(data["ccode"])


@socketio.on("add calendar")
def on_add_calendar(data):
    """
    add a new calendar for user
    """
    print(data)
    userid = data["userid"]
    private = data["privateCal"]
    ccode_list = data["ccode_list"]
    print(ccode_list)
    print(private)
    ccode = add_calendar_for_user(userid, private)
    print(
        "Added calendar for user ",
        userid,
        "With ccode ",
        ccode,
        " Private flag: ",
        private,
    )
    added_event_id = add_event(
        [ccode], "Created Calendar At", 946688461, 946688461, "some words"
    )
    print(added_event_id)
    ccode_list.append(ccode)
    emit_events_to_calender("recieve all events", ccode_list)

    socketio.emit(
        "update dropdown",
        {
            "ccode": ccode,
        },
    )


@socketio.on("get events")
def send_events_to_calendar(data):
    """
    send_events_to_calendar.
    """
    print("LOOKING FOR CALCODE: ", data)
    # EMIT EVENTS TO CALENDAR
    emit_events_to_calender("recieve all events", data)
    print("SENT EVENTS!")


@socketio.on("get ccode details")
def send_ccode_to_calendar(data):
    """
    send_ccode_to_calendar.
    """
    print("getting details for ccode: ", data)
    emit_ccode_to_calender("recieve ccode details", data)
    print("SENT ccode!")


@socketio.on("new event")
def on_new_event(data):
    """
    add a new event for to calendar
    """
    print(data)
    title = data["title"]
    start = data["start"]
    end = data["end"]
    ccode = data["ccode"]
    print(start)
    print(end)
    added_event_id = add_event([ccode], title, start, end, "some words")
    print("SENDING INDIVIDUAL EVENT")
    socketio.emit(
        "calender_event",
        {
            "title": title,
            "start": start,
            "end": end,
            "eventid": added_event_id,
            "ccode": [ccode],
        },
        room=get_sid(),
    )
    return added_event_id


@socketio.on("modify event")
def on_modify_event(data):
    """
    add a new event for to calendar
    """
    print(data)
    title = data["title"]
    start = data["start"]
    end = data["end"]
    ccode = data["ccode"]
    event_id = data["event_id"]
    ccode_list = data["ccode_list"]
    print(start)
    print(end)
    mod_event([ccode], title, start, end, "some words", event_id)
    # EMIT EVENTS TO CALENDAR
    print("print form mod event")
    print(type(ccode_list))
    emit_events_to_calender("recieve all events", ccode_list)


@socketio.on("delete event")
def on_delete_event(data):
    """
    add a new event for to calendar
    """
    print("Recieved request to delete event.")
    print(data)
    event_id = data["event_id"]
    ccode = data["ccode"]
    ccode_list = data["ccode_list"]
    del_event(event_id, [ccode])
    # EMIT EVENTS TO CALENDAR
    print("emit form delete event")
    emit_events_to_calender("recieve all events", ccode_list)


@socketio.on("cCodeToMerge")
def on_merge_calendar(data):
    """
    merge calendar
    """
    ccode_list = data["ccode_list"]
    merge_code = int(data["userToMergeWith"])
    print("LOOKING FOR CALCODE", data["userToMergeWith"])
    cal_code = int(data["currentUser"])
    exists = exists_in_calender(merge_code)
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

        print("cal_code appended")
        ccode_list.append(merge_code)
        print(ccode_list)

        emit_events_to_calender("recieve all events", ccode_list)
    except ValueError:
        print(
            "Ccode does not exist, or you have attempted to merge with a private calendar."
        )


@socketio.on("Import Calendar")
def on_import_calendar(data):
    """
    import primary google calendar for user
    """
    access_token = data["accessToken"]
    private = data["privateCal"]
    userid = data["userid"]
    ccode_list = data["ccode_list"]
    creds = client.AccessTokenCredentials(access_token, "my-user-agent/1.0")
    service = build("calendar", "v3", credentials=creds)
    print("Getting all primary calendar events")
    events_result = (
        service.events()
        .list(calendarId="primary", singleEvents=True, orderBy="startTime")
        .execute()
    )
    events = events_result.get("items", [])
    if not events:
        print("No upcoming events found. Initializing empty calendar.")
    ccode = add_calendar_for_user(userid, private)
    ccode_list.append(ccode)
    for event in events:
        if (
            event["start"].get("dateTime") is None
            or event["end"].get("dateTime") is None
        ):
            continue
        start = int(rfc3339_to_unix(str(event["start"].get("dateTime"))))
        end = int(rfc3339_to_unix(str(event["end"].get("dateTime"))))
        try:
            title = (
                (event["summary"][:117] + "..")
                if len(event["summary"]) > 117
                else event["summary"]
            )
        except KeyError:
            event["summary"] = "No Title"
        try:
            desc = (
                (event["description"][:117] + "..")
                if len(event["description"]) > 117
                else event["description"]
            )
        except KeyError:
            desc = "some desc"
        addedEventId = add_event([ccode], title, start, end, desc)
        print(addedEventId)
    emit_events_to_calender("recieve all events", ccode_list)
    socketio.emit(
        "update dropdown",
        {
            "ccode": ccode,
        },
    )


@socketio.on("modify calendar")
def on_modify_calendar(data):
    """
    modify calendars
    """
    print(data)
    ccode = data["ccode"]
    private = data["privateCal"]
    delete_cal = data["deleteCal"]
    all_ccodes = data["allCcodes"]

    print(ccode)
    calendar = (
        db.session.query(models.Calendars)
        .filter(models.Calendars.ccode == ccode)
        .first()
    )
    if calendar:
        if delete_cal:
            for record in (
                db.session.query(models.Event)
                .filter(models.Event.ccode.contains([ccode]))
                .all()
            ):
                if record.ccode[0] == ccode:
                    del_event(record.id, ccode)
            db.session.query(models.Calendars).filter(
                models.Calendars.ccode == ccode
            ).delete()
        elif private:
            calendar.private = True
        elif private:
            calendar.private = False
        db.session.commit()
        emit_events_to_calender("recieve all events", all_ccodes)


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
