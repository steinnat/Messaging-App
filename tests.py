"""
Messenger App Unit Test Cases for RESTFUL API.
Prerequisite:
    1: Reset Database File
        -flask init-db
    2: Set FLASK_APP environment variable 
        -set FLASK_APP=messenger.py
        -export FLASK_APP=messenger.py
    3: Start server
        -flask run
    4: Open second terminal, run tests
        -python tests.py
Execute Test cases.
    python tests.py
"""

# Python import
import json
import unittest
import requests


class TestMessenger(unittest.TestCase):

    def test_create_thread(self):
        """
        POST: Create Thread
        """
        # Create Thread
        thread_response = requests.post("http://127.0.0.1:5000/thread", data=dict(username="TestUserName"), headers={"RETURN": "1"})
        thread = json.loads(thread_response.content)
        self.assertTrue("thread_id" in thread)

    def test_get_thread_messages(self):
        """
        GET: Get Thread Messages
        """
        # Create Thread
        thread_response = requests.post("http://127.0.0.1:5000/thread", data=dict(username="TestUserName"), headers={"RETURN": "1"})
        thread = json.loads(thread_response.content)["thread_id"]
        username="TestUserName"

        # Send Message In Thread
        requests.post(f"http://127.0.0.1:5000/thread/{thread}/{username}", data=dict(message="Test Message!"))

        # Get Thread Messages
        messages_response = requests.get(f"http://127.0.0.1:5000/thread/{thread}", headers={"RETURN": "1"})
        messages = json.loads(messages_response.content)
        self.assertTrue("messages" in messages)

    def test_send_message_in_thread(self):
        """
        POST: Create Message In Thread
        """
        # Create Thread
        thread_response = requests.post("http://127.0.0.1:5000/thread", data=dict(username="TestUserName"), headers={"RETURN": "1"})
        thread = json.loads(thread_response.content)["thread_id"]
        username="TestUserName"

        # Send Message In Thread
        message_response = requests.post(f"http://127.0.0.1:5000/thread/{thread}/{username}", data=dict(message="Test Message!"))
        message_response = int(json.loads(message_response.content))
        self.assertTrue(message_response == 204)


if __name__ == "__main__":
    unittest.main()
