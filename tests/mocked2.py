'''
    api_mocks.py
    This file tests twitter_query.py.
'''
# pylint: disable=wrong-import-position
# pylint: disable=import-error
# pylint: disable=no-self-use
# pylint: disable=too-few-public-methods
# pylint: disable=unused-argument
import unittest
import unittest.mock as mock
import sys
import os
sys.path.append(os.path.abspath(os.path.join('..')))
import app
from alchemy_mock.mocking import AlchemyMagicMock

KEY_INPUT = "arg1"
KEY_INPUT2 = "arg2"
KEY_INPUT3 = "arg3"
KEY_EXPECTED = "expected"
KEY_MESSAGE = "message"
KEY_USER = "user"
KEY_PFP = "pfp_url"

# def mocked_requests_get_dad(*args, **kwargs):
#     '''
#     Creates mocked request for dad api.
#     '''
#     class MockedDadResponse:
#         '''
#         Defines MockedDadResponse.
#         '''
#         def __init__(self, json_data, status):
#             self.json_data = json_data
#             self.status = status
#         def json(self):
#             '''
#             Defines the return response of a json().
#             '''
#             return self.json_data
#     if args[0] == 'https://icanhazdadjoke.com/':
#         return MockedDadResponse({"joke":"My dog used to chase people \
# on a bike a lot. It got so bad I had to take his bike away."}, 200)
#     return MockedDadResponse(None, 404)
# def mocked_requests_funtranslate(*args, **kwargs):
#     '''
#     Creates mocked request for funtranslate api.
#     '''
#     class MockedFunResponse:
#         '''
#         Defines MockedFunResponse.
#         '''
#         def __init__(self, json_data, status):
#             self.json_data = json_data
#             self.status = status
#         def json(self):
#             '''
#             Defines response return .json()
#             '''
#             return self.json_data
#     return MockedFunResponse({"contents": {"translated": "Welcome to Macca's"}}, 200)
# def mocked_requests_anime(*args, **kwargs):
#     '''
#     Creates mocked request for jikan API.
#     '''
#     class MockedAnimeResponse:
#         '''
#         Defines MockedAnimeResponse.
#         '''
#         def __init__(self, dict_data, status):
#             self.dict_data = dict_data
#             self.status = status
#         def ret_data(self):
#             '''
#             Returns anime response return type.
#             '''
#             return self.dict_data
#     return MockedAnimeResponse({'results':\
#     [{'title': 'Shoujo Shuumatsu Ryokou', 'score': 8.19, 'synopsis': \
# 'Amid the desolate remains of a once-thriving city, \
# only the rumbling of a motorbike breaks the cold '}]}, \
#     200).ret_data()

# class DadQueryTestCase(unittest.TestCase):
#     '''
#     Sets up test cases for dad api.
#     '''
#     def setUp(self):
#         '''
#         Sets up paramters for dad cases.
#         '''
#         self.success_test_params = [
#             {
#               KEY_INPUT: "!! dad",
#                 KEY_INPUT2: "",
#                 KEY_EXPECTED: {
#                     KEY_MESSAGE: "My dog used to chase people on \
# a bike a lot. It got so bad I had to take his bike away.",
#                     KEY_USER: "Bot",
#                     KEY_PFP: "<img src=" + "\"./botpfp.png\">",
#                 }
#             }
#         ]
#     def test_chatbot_dad_success(self):
#         '''
#         Success cases for dad.
#         '''
#         for test_case in self.success_test_params:
#             with mock.patch('requests.get', mocked_requests_get_dad):
#                 response = chatbot.CoolBot().is_command(test_case[KEY_INPUT], "")
#             expected = test_case[KEY_EXPECTED]
#             self.assertDictEqual(response, expected)
# class FunQueryTestCase(unittest.TestCase):
#     '''
#     Creates test cases for funtranslate api.
#     '''
#     def setUp(self):
#         '''
#         Sets up parameters for cases.
#         '''
#         self.success_test_params = [
#             {
#               KEY_INPUT: "!! funtranslate Welcome to McDonald's",
#                 KEY_INPUT2: "",
#                 KEY_EXPECTED: {
#                     KEY_MESSAGE: "Welcome to Macca's",
#                     KEY_USER: "Bot",
#                     KEY_PFP: "<img src=" + "\"./botpfp.png\">",
#                 }
#             }
#         ]
#         self.failure_test_params = [
#             {
#               KEY_INPUT: "!! funtranslate",
#                 KEY_INPUT2: "",
#                 KEY_EXPECTED: {
#                     KEY_MESSAGE: "Welcome to Macca's",
#                     KEY_USER: "Bot",
#                     KEY_PFP: "<img src=" + "\"./botpfp.png\">",
#                 }
#             }
#         ]
#     def test_chatbot_fun_success(self):
#         '''
#         Success cases for funtranslate
#         '''
#         for test_case in self.success_test_params:
#             with mock.patch('requests.get', mocked_requests_funtranslate):
#                 response = chatbot.CoolBot().is_command(test_case[KEY_INPUT], "")
#             expected = test_case[KEY_EXPECTED]
#             self.assertDictEqual(response, expected)
#     def test_chatbot_fun_failure(self):
#         '''
#         Failure cases for funtranslate
#         '''
#         for test_case in self.failure_test_params:
#             with mock.patch('requests.get', mocked_requests_funtranslate):
#                 response = chatbot.CoolBot().is_command(test_case[KEY_INPUT], "")
#             expected = test_case[KEY_EXPECTED]
#             self.assertNotEqual(response, expected)
# class AnimeQueryTestCase(unittest.TestCase):
#     '''
#     Creates test cases for jikan API.
#     '''
#     def setUp(self):
#         '''
#         Sets up parameters for cases.
#         '''
#         self.success_test_params = [
#             {
#               KEY_INPUT: "!! anime Girl's Last Tour",
#                 KEY_INPUT2: "",
#                 KEY_EXPECTED: {
#                     KEY_MESSAGE: "Title: "\
#                     + "Shoujo Shuumatsu Ryokou"\
#                     + "<br></br>Score: "\
#                     + "8.19"\
#                     + "<br></br>Summary: "\
#                     + "Amid the desolate remains of a once-thriving city, \
# only the rumbling of a motorbike breaks the cold "\
#                     + "...",
#                     KEY_USER: "Bot",
#                     KEY_PFP: "<img src=" + "\"./botpfp.png\">",
#                 }
#             }
#         ]
#         self.failure_test_params = [
#             {
#               KEY_INPUT: "!! anime",
#                 KEY_INPUT2: "",
#                 KEY_EXPECTED: {
#                     KEY_MESSAGE: "Title: "\
#                     + "Shoujo Shuumatsu Ryokou"\
#                     + "<br></br>Score: "\
#                     + "8.19"\
#                     + "<br></br>Summary: "\
#                     + "Amid the desolate remains of a once-thriving city, \
# only the rumbling of a motorbike breaks the cold "\
#                     + "...",
#                     KEY_USER: "Bot",
#                     KEY_PFP: "<img src=" + "\"./botpfp.png\">",
#                 }
#             }
#         ]
#     def test_chatbot_anime_success(self):
#         '''
#         Success cases for Jikan.
#         '''
#         for test_case in self.success_test_params:
#             with mock.patch('jikanpy.Jikan.search', mocked_requests_anime):
#                 response = chatbot.CoolBot().is_command(test_case[KEY_INPUT], "")
#             expected = test_case[KEY_EXPECTED]
#             self.assertDictEqual(response, expected)
#     def test_chatbot_anime_failure(self):
#         '''
#         Failure cases for Jikan.
#         '''
#         for test_case in self.failure_test_params:
#             with mock.patch('jikanpy.Jikan.search', mocked_requests_anime):
#                 response = chatbot.CoolBot().is_command(test_case[KEY_INPUT], "")
#             expected = test_case[KEY_EXPECTED]
#             self.assertNotEqual(response, expected)
class SQLQueryTestCase(unittest.TestCase):
    '''
    Sets up test cases for DB calls.
    '''
    def setUp(self):
        '''
        Sets up parameters for dad cases.
        '''
        self.success_test_params = [
            {
                KEY_INPUT: 1,
                KEY_INPUT2: "New Event",
                KEY_INPUT3: "dfb8@njit.edu",
                KEY_EXPECTED: None
            }
        ]
        self.success_test_params_emit = [
            {
                KEY_INPUT: "test_channel",
                KEY_EXPECTED: None
            }
        ]
    def mock_emit(self, channel, test_dict):
        '''
        Mocks out emits.
        '''
        print("Emitted on channel.")
        return {"channel": channel, "test_dict": test_dict}
    def test_push_new_event_to_db(self):
        '''
        Success cases for push_new_user_to_db.
        '''
        for test_case in self.success_test_params:
            with mock.patch('app.db', AlchemyMagicMock()):
                response = app.push_new_user_to_db\
                (test_case[KEY_INPUT], test_case[KEY_INPUT2], test_case[KEY_INPUT3])
            expected = test_case[KEY_EXPECTED]
            self.assertEqual(response, expected)
    def test_emit_all_history(self):
        '''
        Success cases for emitting all history.
        '''
        for test_case in self.success_test_params:
            with mock.patch('app.db', AlchemyMagicMock()):
                with mock.patch('app.socketio.emit', self.mock_emit):
                    response = app.emit_all_history(test_case[KEY_INPUT])
            expected = test_case[KEY_EXPECTED]
            self.assertEqual(response, expected)
# class GoogleLoginTestCase(unittest.TestCase):
#     '''
#     Sets up test cases Google Oauth.
#     '''
#     def setUp(self):
#         '''
#         Sets up parameters for dad cases.
#         '''
#         self.success_test_params = [
#             {
#                 KEY_INPUT: {"name": "Koomi", "email":\
#                 "baconatoring@gmail.com", "idtoken": "good_mock_token"},
#                 KEY_EXPECTED: "mock_id"
#             }
#         ]
#         self.failure_test_params = [
#             {
#                 KEY_INPUT: {"name": "Koomi", "email":\
#                 "baconatoring@gmail.com", "idtoken": "bad_mock_token"},
#                 KEY_EXPECTED: "Unverified."
#             },
#             {
#                 KEY_INPUT: {"name": "Koomi", "email":\
#                 "baconatoring@gmail.com", "idtoken": "vvmock_token"},
#                 KEY_EXPECTED: "Unverified."
#             }
#         ]
#     def mocked_verify(self, *args, **kwargs):
#         '''
#         Creates a mocked Google verification.
#         '''
#         if args[0]=="good_mock_token":
#             return {"sub": "mock_id"}
#         if args[0]=="bad_mock_token":
#             return {"false": False}
#         raise ValueError
#     def mocked_flask(self):
#         '''
#         Mocks out flask sid request.
#         '''
#         class MockedFlaskServer:
#             '''
#             Mocks a flask server with a fake sid.
#             '''
#             def __init__(self, sig_id):
#                 self.sig_id=sig_id
#             def sid(self):
#                 '''
#                 Returns sid of fake server.
#                 '''
#                 return self.sig_id

#         return MockedFlaskServer("1234").sid()
#     def test_on_new_google_user_success(self):
#         '''
#         Success cases for on_new_google_user.
#         '''
#         for test_case in self.success_test_params:
#             with mock.patch('google.oauth2.id_token.verify_oauth2_token', self.mocked_verify):
#                 with mock.patch('app.get_sid', self.mocked_flask):
#                     with mock.patch('app.db', AlchemyMagicMock()):
#                         response = app.on_new_google_user(test_case[KEY_INPUT])
#             expected = test_case[KEY_EXPECTED]
#             self.assertEqual(response, expected)
#     def test_on_new_google_user_failure(self):
#         '''
#         Failure cases for on_new_google_user.
#         '''
#         for test_case in self.failure_test_params:
#             with mock.patch('google.oauth2.id_token.verify_oauth2_token', self.mocked_verify):
#                 with mock.patch('app.get_sid', self.mocked_flask):
#                     with mock.patch('app.db', AlchemyMagicMock()):
#                         response = app.on_new_google_user(test_case[KEY_INPUT])
#             expected = test_case[KEY_EXPECTED]
#             self.assertEqual(response, expected)
# class NewMessageTestCase(unittest.TestCase):
#     '''
#     Sets up test cases new messages.
#     '''
#     def setUp(self):
#         '''
#         Sets up paramters for message cases.
#         '''
#         self.success_test_params = [
#             {
#               KEY_INPUT: {"message": "!! about", "user": "Koomi", "pfp_url":\
#               "<img src=" + "\"https://www.fakepfp.com/fakepfp.png\">"},
#                 KEY_EXPECTED: {
#                     KEY_MESSAGE: "!! about",
#                     KEY_USER: "Koomi",
#                     KEY_PFP: "<img src=" + "\"https://www.fakepfp.com/fakepfp.png\">",
#                 }
#             },
#             {
#               KEY_INPUT: {"message": "https://www.streamscheme.com/wp-content/"\
#               +"uploads/2020/04/poggers.png", "user": "Koomi", "pfp_url":\
#               "<img src=" + "\"https://www.fakepfp.com/fakepfp.png\">"},
#                 KEY_EXPECTED: {
#                     KEY_MESSAGE: "<a href=" + "\"https://www.streamscheme.com/wp-content"\
#                     +"/uploads/2020/04/poggers.png\">https://www.streamscheme.com/"\
#                     +"wp-content/uploads/2020/04/poggers.png</a>",
#                     KEY_USER: "Koomi",
#                     KEY_PFP: "<img src=" + "\"https://www.fakepfp.com/fakepfp.png\">",
#                 }
#             }
#         ]
#     def test_new_message_success(self):
#         '''
#         Success cases for messages.
#         '''
#         for test_case in self.success_test_params:
#             with mock.patch('app.db', AlchemyMagicMock()):
#                 response = app.on_new_message(test_case[KEY_INPUT])
#             expected = test_case[KEY_EXPECTED]
#             self.assertDictEqual(response, expected)
# class ConnectTestCases(unittest.TestCase):
#     '''
#     Sets up test cases connect functions.
#     '''
#     def setUp(self):
#         '''
#         Sets up paramters for connection test cases.
#         '''
#         self.success_test_params_on_connect = [
#             {
#                 KEY_EXPECTED: {"channel": "connected", "test_dict": {"test": "Connected"}}
#             },
#         ]
#         self.success_test_params_on_disconnect = [
#             {
#                 KEY_EXPECTED: {"channel": "user change", "test_dict": 0}
#             },
#         ]
#     def mock_emit(self, channel, test_dict):
#         '''
#         Mocks out emits.
#         '''
#         print("Emitted on channel.")
#         return {"channel": channel, "test_dict": test_dict}
#     def test_on_connect(self):
#         '''
#         Success cases for on_connect.
#         '''
#         for test_case in self.success_test_params_on_connect:
#             with mock.patch('app.socketio.emit', self.mock_emit):
#                 response = app.on_connect()
#             expected = test_case[KEY_EXPECTED]
#             self.assertEqual(response, expected)
#     def test_on_disconnect(self):
#         '''
#         Success cases for on_connect.
#         '''
#         for test_case in self.success_test_params_on_disconnect:
#             with mock.patch('app.socketio.emit', self.mock_emit):
#                 response = app.on_disconnect()
#             expected = test_case[KEY_EXPECTED]
#             self.assertEqual(response, expected)

if __name__ == '__main__':
    unittest.main()
