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

APP = flask.Flask(__name__)

##BOILER PLATE CODE TO INITIATE SOCKETS
SOCKETIO = flask_socketio.SocketIO(APP)
SOCKETIO.init_app(APP, cors_allowed_origins="*")

DOTENV_PATH = join(dirname(__file__), "sql.env")
load_dotenv(DOTENV_PATH)

# BOILER PLATE CODE TO INSTANTIATE PSQL AND SQLALCHEMY

DATABASE_URI = os.environ["DATABASE_URL"]

APP.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI

DB = flask_sqlalchemy.SQLAlchemy(APP)

DB.init_app(APP)
DB.app = APP


CALENDER_EVENT_CHANNEL = "calendar_event"

import models


def push_new_user_to_database(ident, name, email):
    """
    Pushes new user to database.
    """
    DB.session.add(models.AuthUser(ident, name, email))
    DB.session.commit()


def add_event(ccode, title, start, end, desc):
    """
    adds an event, returns id of added event
    """
    added_event = models.Event(ccode, title, start, end, desc)
    DB.session.add(added_event)
    DB.session.commit()
    return added_event.id


def mod_event(ccode, title, start, end, desc, event_id):
    """
    modifies an event, returns id of added event
    """
    event = DB.session.query(models.Event).filter(models.Event.id == event_id).first()
    event.id = event_id
    event.title = title
    event.ccode = ccode
    event.start = start
    event.end = end
    event.desc = desc
    DB.session.commit()
    emit_events_to_calender("recieve all events", ccode)


def del_event(event_id, ccode):
    """
    Deletes an event and returns the id of the deleted event.
    """
    DB.session.query(models.Event).filter(models.Event.id == event_id).delete()
    DB.session.commit()


def delete_cal(ccode):
    """
    Deletes an cal
    """
    print("Deleting all events!")
    print(":GOT HERE GOT HERE GOT HERE GOT HERE")
    for record in (
            DB.session.query(models.Event).filter(models.Event.ccode.contains(ccode)).all()
    ):
        print(record)
    DB.session.query(models.Calendars).filter(models.Calendars.ccode == ccode).delete()
    DB.session.commit()


def add_calendar_for_user(userid, priv_flag):

    """
    adds an event, returns the ccode of the new calendar
    """
    added_calendar = models.Calendars(userid, priv_flag)
    DB.session.add(added_calendar)
    DB.session.commit()
    return added_calendar.ccode


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
            for record in DB.session.query(models.Event)
            .filter(models.Event.ccode.contains([ccode]))
            .all()
        ]
        all_events.extend(events_for_ccode)

    all_events = list(unique_everseen(all_events))
    # for event in all_events:
    #     print(event)
    SOCKETIO.emit(channel, all_events, room=sid)


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
            DB.session.query(models.Calendars)
            .filter(models.Calendars.ccode == ccode)
            .first()
        )
        details_for_ccode = {
            "userid": record.userid,
            "private": record.private,
        }
        ccode_details[record.ccode] = details_for_ccode

    if len(ccode_details) > 0:
        SOCKETIO.emit(channel, ccode_details, room=sid)


def exists_in_auth_user(check_id):
    """
    Check to see if the auth user is there
    """
    return (
        DB.session.query(models.AuthUser.userid).filter_by(userid=check_id).scalar()
        is not None
    )


def exists_in_calender(merge_code):
    """
    Check to see if merge calendar exists
    """
    return (
        DB.session.query(models.Calendars.ccode).filter_by(ccode=merge_code).scalar()
        is not None
    )


##SOCKET EVENTS
@SOCKETIO.on("connect")
def on_connect():
    """
    Runs on connect.
    """
    # print("Someone connected!")


@SOCKETIO.on("disconnect")
def on_disconnect():
    """
    Runs on disconnect.
    """
    # print("Someone disconnected!")


@SOCKETIO.on("new google user")
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
            push_new_user_to_database(userid, name, email)
            add_calendar_for_user(userid, False)
        all_ccodes = [
            record.ccode
            for record in DB.session.query(models.Calendars)
            .filter_by(userid=userid)
            .all()
        ]
        SOCKETIO.emit(
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


@SOCKETIO.on("delete calendar")
def on_delete_cal(data):
    """
    add a new event for to calendar
    """
    print("not updating?")
    delete_cal(data["ccode"])


@SOCKETIO.on("add calendar")
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

    SOCKETIO.emit(
        "update dropdown",
        {
            "ccode": ccode,
        },
    )


@SOCKETIO.on("get events")
def send_events_to_calendar(data):
    """
    send_events_to_calendar.
    """
    print("LOOKING FOR CALCODE: ", data)
    # EMIT EVENTS TO CALENDAR
    emit_events_to_calender("recieve all events", data)
    print("SENT EVENTS!")


@SOCKETIO.on("get ccode details")
def send_ccode_to_calendar(data):
    """
    send_ccode_to_calendar.
    """
    print("getting details for ccode: ", data)
    emit_ccode_to_calender("recieve ccode details", data)
    print("SENT ccode!")


@SOCKETIO.on("new event")
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
    SOCKETIO.emit(
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


@SOCKETIO.on("modify event")
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


@SOCKETIO.on("delete event")
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


@SOCKETIO.on("cCodeToMerge")
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
                DB.session.query(models.Event)
                .filter(models.Event.ccode.contains([merge_code]))
                .all()
        ):
            if cal_code not in record.ccode:
                record.ccode.append(cal_code)
                DB.session.commit()

        print("cal_code appended")
        ccode_list.append(merge_code)
        print(ccode_list)

        emit_events_to_calender("recieve all events", ccode_list)
    except ValueError:
        print(
            "Ccode does not exist, or you have attempted to merge with a private calendar."
        )


@SOCKETIO.on("Import Calendar")
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
        added_event_id = add_event([ccode], title, start, end, desc)
        print(added_event_id)
    emit_events_to_calender("recieve all events", ccode_list)
    SOCKETIO.emit(
        "update dropdown",
        {
            "ccode": ccode,
        },
    )


@SOCKETIO.on("modify calendar")
def on_modify_calendar(data):
    """
    modify calendar
    """
    print(data)
    ccode = data["ccode"]
    private = data["privateCal"]
    del_cal = data["deleteCal"]
    all_ccodes = data["allCcodes"]

    print(ccode)
    calendar = (
        DB.session.query(models.Calendars)
        .filter(models.Calendars.ccode == ccode)
        .first()
    )
    if calendar:
        if del_cal:
            for record in (
                    DB.session.query(models.Event)
                    .filter(models.Event.ccode.contains([ccode]))
                    .all()
            ):
                if record.ccode[0] == ccode:
                    del_event(record.id, ccode)
            DB.session.query(models.Calendars).filter(
                models.Calendars.ccode == ccode
            ).delete()
        elif private:
            calendar.private = True
        elif private:
            calendar.private = False
        DB.session.commit()
        emit_events_to_calender("recieve all events", all_ccodes)


@APP.route("/")
def hello():
    """
    Runs at page-load.

    """
    models.DB.create_all()
    DB.session.commit()
    print("User has joined.")
    return flask.render_template("index.html")


if __name__ == "__main__":
    SOCKETIO.run(
        APP,
        host=os.getenv("IP", "0.0.0.0"),
        port=int(os.getenv("PORT", "8080")),
        debug=True,
    )
