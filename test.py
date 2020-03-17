import unittest

from app import app


class BasicTestCase(unittest.TestCase):
    def setup(self):
        tester = app.test_client(self)
        app.config["SECRET_KEY"] = "!@#$%^&*"
        app.config["UPLOAD_FOLDER"] = "images/"
        app.config["DEBUG"] = False

    def test_main_page(self):
        tester = app.test_client(self)
        response = tester.get("/")
        self.assertEqual(response.status_code, 200)

    def test_register_page(self):
        tester = app.test_client(self)
        response = tester.get("/signup")
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        tester = app.test_client(self)
        response = tester.post(
            "/signup", data=dict(email="someuser@gmail.com", password="pass123")
        )
        self.assertEqual(response.status_code, 200)

    
        


if __name__ == "__main__":
    unittest.main()
