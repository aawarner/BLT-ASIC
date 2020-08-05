import flask_unsign
import re
import unittest
import webui
import time


class Webui(unittest.TestCase):
    def setUp(self):
        # creates a test client
        self.app = webui.app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True


    def test_status_codes(self):
        # Test app routes
        result = self.app.get("/")
        self.assertEqual(result.status_code, 200)

        result = self.app.get("/logout")
        self.assertEqual(result.status_code, 302)

        result = self.app.get("/clearcsv")
        self.assertEqual(result.status_code, 302)

        result = self.app.get("/clearwebsn")
        self.assertEqual(result.status_code, 302)

        result = self.app.get("/clearso")
        self.assertEqual(result.status_code, 302)

        result = self.app.get("/clearsn")
        self.assertEqual(result.status_code, 302)

        result = self.app.get("/clearscan")
        self.assertEqual(result.status_code, 302)

        result = self.app.get("/ccwrresults")
        self.assertEqual(result.status_code, 200)

        result = self.app.get("/serialnumber")
        self.assertEqual(result.status_code, 200)

        result = self.app.post("/serialnumber")
        self.assertEqual(result.status_code, 200)

        result = self.app.get("/salesorder")
        self.assertEqual(result.status_code, 200)

        result = self.app.post("/salesorder")
        self.assertEqual(result.status_code, 200)

        result = self.app.get("/scan")
        self.assertEqual(result.status_code, 200)

        result = self.app.get("/scanupload")
        self.assertEqual(result.status_code, 200)

        result = self.app.post("/scanupload")
        self.assertEqual(result.status_code, 200)

        result = self.app.get("/help")
        self.assertEqual(result.status_code, 200)

        result = self.app.get("/teamsupport")
        self.assertEqual(result.status_code, 302)

    def test_login_logout(self):
        # Test invalid login
        username = "test"
        password = "test"
        sadomain = "test"

        result = self.app.post("/login", data=dict(username=username, password=password, SADomain=sadomain),
                               follow_redirects=True)
        self.assertIn(b"Invalid Credentials...Try again", result.data)

        # Test logout
        result = self.app.get("/logout")
        cookie = str(result.headers.getlist('Set-Cookie'))
        pattern = "(?<==)[^;]*"
        cookie = re.search(pattern, cookie)
        cookie = cookie.group(0)
        session = {}
        session.update(flask_unsign.decode(cookie))
        self.assertEqual(session.get("logged_in"), False)


if __name__ == '__main__':
    unittest.main()
