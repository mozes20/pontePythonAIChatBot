import unittest
import pytest
import time
from app.ai_services.ai_service import AiService

from app.models import models

from fastapi.testclient import TestClient
from app.main import app
import json

client = TestClient(app)

class TestAiService(unittest.TestCase):
    def setUp(self):
        self.ai_service = AiService()

    def test_convert_to_ai_communication_schema(self):
        ai_chat_bot_contents = [models.AiChatBotContent(chat_id=2, question="question1", answer="answer1"),
                                models.AiChatBotContent(chat_id=2, question="question2", answer="answer2")]

        expected_result = [
            {"role": "system", "content": 'You are a intelligent assistant.'},
            {"role": "user", "content": "question1"},
            {"role": "assistant", "content": "answer1"},
            {"role": "user", "content": "question2"},
            {"role": "assistant", "content": "answer2"}
        ]

        result = self.ai_service.convert_to_ai_communication_schema(ai_chat_bot_contents)
        self.assertEqual(result, expected_result)

    def test_dummy_ai(self):

        username = "htcmokka@gmail.com"
        password = "Mozes"
        token = self.get_token(username, password)
        # Define a sample request body
        request_data = {
            "chat_id": 0,
            "text": "sample_text"
        }

        # Send a POST request to the /mock-ai endpoint
        response = client.post("ai/mock-ai", data=json.dumps(request_data),headers={"Authorization": f"Bearer {token}"}, json={"text": "test"})

        # Assert that the response status code is 200
        assert response.status_code == 200
        assert response.json() == {"reply": "Mock AI response to 'sample_text'"}

    def test_rate_limit(self):
        username = "htcmokka@gmail.com"
        password = "Mozes"
        token = self.get_token(username, password)

        for _ in range(3):
            response = client.post("ai/mock-ai", headers={"Authorization": f"Bearer {token}"}, json={"text": "test"})
            assert response.status_code == 200

        # The fourth request should be rate limited
        response = client.post("ai/mock-ai", headers={"Authorization": f"Bearer {token}"}, json={"text": "test"})
        assert response.status_code == 429

        # Wait for the rate limit to reset
        time.sleep(60)

        # After waiting, we should be able to make requests again
        response = client.post("ai/mock-ai", headers={"Authorization": f"Bearer {token}"}, json={"text": "test"})
        assert response.status_code == 200

    def get_token(self, username: str, password: str):
        # Try to register a new user
        register_response = client.post("auth/register", json={"email": username, "password": password})

        # If the user already exists, the register endpoint should return a status code of 400 or similar
        # In this case, we just ignore the error and proceed to log in
        if register_response.status_code != 200:
            print("User already exists, proceeding to log in")

        # Log in as the user
        login_response = client.post("auth/login", data={"username": username, "password": password})

        # Extract the token from the login response
        token = login_response.json().get("access_token")
        print(token)
        return token

if __name__ == '__main__':
    unittest.main()