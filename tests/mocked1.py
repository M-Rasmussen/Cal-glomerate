"""
    api_mocks.py
    This file tests many database functions for storing events and calendars.
"""
# pylint: disable=wrong-import-position
# pylint: disable=import-error
# pylint: disable=no-self-use
# pylint: disable=too-few-public-methods
# pylint: disable=unused-argument
import unittest
import unittest.mock as mock
import sys
import os

sys.path.append(os.path.abspath(os.path.join("..")))
import app
import models
from alchemy_mock.mocking import AlchemyMagicMock

KEY_INPUT = "arg1"
KEY_INPUT2 = "arg2"
KEY_INPUT3 = "arg3"
KEY_INPUT4 = "arg4"
KEY_INPUT5 = "arg5"
KEY_EXPECTED = "expected"
KEY_MESSAGE = "message"
KEY_USER = "user"
KEY_PFP = "pfp_url"


class SQLQueryTestCase(unittest.TestCase):
    """
    Sets up test cases for DB calls.
    """

    def setUp(self):
        """
        Sets up parameters for dad cases.
        """
        self.success_test_params_event = [
            {
                KEY_INPUT: [1],
                KEY_INPUT2: "New Event",
                KEY_INPUT3: "1605290154",
                KEY_INPUT4: "1605290054",
                KEY_INPUT5: "some text",
                KEY_EXPECTED: None,
            }
        ]
        self.success_test_params_user = [
            {
                KEY_INPUT: 1,
                KEY_INPUT2: "Name",
                KEY_INPUT3: "name@njit.edu",
                KEY_EXPECTED: None,
            }
        ]
        self.success_test_params_cal = [{KEY_INPUT: 1, KEY_INPUT2: True, KEY_EXPECTED: None}]
        self.success_test_params_emit = [
            {KEY_INPUT: "test_channel", KEY_INPUT2: [1], KEY_EXPECTED: None}
        ]
        self.success_test_params_send_events_to_cal = [
            {KEY_INPUT: "test_channel", KEY_INPUT2: [1], KEY_EXPECTED: None}
        ]
        self.success_test_params_on_new_event = [
            {
                KEY_INPUT: {
                    "title": "Mocked incoming event!",
                    "date": "Nov 19 3000 Fake Date",
                    "start": "1605290154",
                    "end": "1605290054",
                    "ccode": "99",
                },
                KEY_EXPECTED: None,
            }
        ]
        self.success_test_params_on_new_merge = [
            {
                KEY_INPUT: {"userToMergeWith": "99", "currentUser": "98", "ccode_list": [1,2,3]},
                KEY_EXPECTED: None,
            }
        ]
        self.sucess_test_params_check_id = [
            {
                KEY_INPUT:{
                    "check_id": "1",
                },
                KEY_EXPECTED:True,
            },]

    def mock_emit(self, channel, test_dict, room="-1"):
        """
        Mocks out emits.
        """
        print("Emitted on channel." + room)
        return {"channel": channel, "test_dict": test_dict}

    def mock_sid(self):
        sid = "fake sid"
        print("returning: " + sid)
        return sid

    def mocked_exists(self, userid):
        """"Mocked out to make sure the user exists in the database"""
        return False
    
    def mocked_emit_events_to_calender(self, channel,cal_code):
        return True


    def test_push_new_user_to_db(self):
        """
        Success cases for push_new_user_to_db.
        """
        for test_case in self.success_test_params_user:
            with mock.patch("app.db", AlchemyMagicMock()):
                response = app.push_new_user_to_db(
                    test_case[KEY_INPUT], test_case[KEY_INPUT2], test_case[KEY_INPUT3]
                )
            expected = test_case[KEY_EXPECTED]
            self.assertEqual(response, expected)

    def test_push_new_cal_to_db(self):
        for test_case in self.success_test_params_cal:
            with mock.patch("app.db", AlchemyMagicMock()):
                response = app.add_calendar_for_user(test_case[KEY_INPUT], test_case[KEY_INPUT2])
            expected = test_case[KEY_EXPECTED]
            self.assertEqual(response, expected)

    def test_push_new_event_to_db(self):
        """
        Success cases for push_new_user_to_db.
        """
        for test_case in self.success_test_params_event:
            with mock.patch("app.db", AlchemyMagicMock()):
                response = app.add_event(
                    test_case[KEY_INPUT],
                    test_case[KEY_INPUT2],
                    test_case[KEY_INPUT3],
                    test_case[KEY_INPUT4],
                    test_case[KEY_INPUT5],
                )
            expected = test_case[KEY_EXPECTED]
            self.assertEqual(response, expected)

    def test_emit_all_history(self):
        """
        Success cases for emitting all history.
        """
        for test_case in self.success_test_params_emit:
            with mock.patch("app.db", AlchemyMagicMock()):
                with mock.patch("app.socketio.emit", self.mock_emit):
                    with mock.patch("app.get_sid", self.mock_sid):
                        response = app.emit_events_to_calender(
                            test_case[KEY_INPUT], test_case[KEY_INPUT2]
                        )
            expected = test_case[KEY_EXPECTED]
            self.assertEqual(response, expected)

    def test_socket_on_new_event(self):
        """
        Success cases for push_new_user_to_db.
        """
        for test_case in self.success_test_params_on_new_event:
            with mock.patch("app.db", AlchemyMagicMock()):
                with mock.patch("app.socketio.emit", self.mock_emit):
                    with mock.patch("app.get_sid", self.mock_sid):
                        response = app.on_new_event(test_case[KEY_INPUT])
            expected = test_case[KEY_EXPECTED]
            self.assertEqual(response, expected)

    def test_on_merge_calendar(self):
        """
        Success cases for push_new_user_to_db.
        """
        for test_case in self.success_test_params_on_new_merge:
            with mock.patch("app.db", AlchemyMagicMock()):
                with mock.patch("app.socketio.emit", self.mock_emit):
                    with mock.patch("app.get_sid", self.mock_sid):
                        with mock.patch("app.exists_in_calender", self.mocked_exists):
                            response = app.on_merge_calendar(test_case[KEY_INPUT])
            expected = test_case[KEY_EXPECTED]
            self.assertEqual(response, expected)

    def test_exists_in_calender(self):
        for test_case in self.sucess_test_params_check_id:
            with mock.patch("app.db", AlchemyMagicMock()):
                response = app.exists_in_calender(
                    test_case[KEY_INPUT])
            expected = test_case[KEY_EXPECTED]
            self.assertEqual(response, expected)

class GoogleLoginTestCase(unittest.TestCase):
    """
    Sets up test cases Google Oauth.
    """

    def setUp(self):
        """
        Sets up parameters for dad cases.
        """
        self.success_test_params_google = [
            {
                KEY_INPUT: {
                    "name": "Koomi",
                    "email": "baconatoring@gmail.com",
                    "idtoken": "good_mock_token",
                },
                KEY_EXPECTED: "mock_id",
            }
        ]
        self.failure_test_params_google = [
            {
                KEY_INPUT: {
                    "name": "Koomi",
                    "email": "baconatoring@gmail.com",
                    "idtoken": "bad_mock_token",
                },
                KEY_EXPECTED: "Unverified.",
            },
            {
                KEY_INPUT: {
                    "name": "Koomi",
                    "email": "baconatoring@gmail.com",
                    "idtoken": "vvmock_token",
                },
                KEY_EXPECTED: "Unverified.",
            },
        ]
        self.sucess_test_params_check_id = [
            {
                KEY_INPUT:{
                    "check_id": "1",
                },
                KEY_EXPECTED:True,
            },]

    def mocked_exists(self, userid):
        """"Mocked out to make sure the user exists in the database"""
        return False

    def mocked_verify(self, *args, **kwargs):
        """
        Creates a mocked Google verification.
        """
        if args[0] == "good_mock_token":
            return {"sub": "mock_id"}
        if args[0] == "bad_mock_token":
            return {"false": False}
        raise ValueError

    def mocked_flask(self):
        """
        Mocks out flask sid request.
        """

        class MockedFlaskServer:
            """
            Mocks a flask server with a fake sid.
            """

            def __init__(self, sig_id):
                self.sig_id = sig_id

            def sid(self):
                """
                Returns sid of fake server.
                """
                return self.sig_id

        return MockedFlaskServer("1234").sid()

    def test_on_new_google_user_success(self):
        """
        Success cases for on_new_google_user.
        """
        for test_case in self.success_test_params_google:
            with mock.patch(
                "google.oauth2.id_token.verify_oauth2_token", self.mocked_verify
            ):
                with mock.patch("app.get_sid", self.mocked_flask):
                    with mock.patch("app.db", AlchemyMagicMock()):
                        with mock.patch("app.exists_in_auth_user", self.mocked_exists):
                            response = app.on_new_google_user(test_case[KEY_INPUT])
            expected = test_case[KEY_EXPECTED]
            self.assertEqual(response, expected)

    def test_on_new_google_user_failure(self):
        """
        Failure cases for on_new_google_user.
        """
        for test_case in self.failure_test_params_google:
            with mock.patch(
                "google.oauth2.id_token.verify_oauth2_token", self.mocked_verify
            ):
                with mock.patch("app.get_sid", self.mocked_flask):
                    with mock.patch("app.db", AlchemyMagicMock()):
                        response = app.on_new_google_user(test_case[KEY_INPUT])
            expected = test_case[KEY_EXPECTED]
            self.assertEqual(response, expected)
    def test_exists_in_auth_user(self):
        """
        Test exists in auth user
        """
        for test_case in self.sucess_test_params_check_id:
            with mock.patch("app.db", AlchemyMagicMock()):
                response = app.exists_in_auth_user(
                    test_case[KEY_INPUT])
            expected = test_case[KEY_EXPECTED]
            self.assertEqual(response, expected)

if __name__ == "__main__":
    unittest.main()
