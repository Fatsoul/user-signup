#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import re
from string import letters
import os

form = """
<!DOCTYPE html>
<html>
    <head>
        <title>User Sign-up</title>
        <style type="text/css">
            .error {
                color: red;
            }
        </style>
    </head>
    <body>
    <h1>
        User Sign-up
    </h1>


        <form method="post">
            <table>
                <tr>
                    <td><label for="username">Username</label></td>
                    <td>
                        <input name="username" type="text" value="%(username)s" >
                        <span class="error">%(error_username)s</span>
                    </td>
                </tr>
                <tr>
                    <td><label for="password">Password</label></td>
                    <td>
                        <input name="password" type="password" >
                        <span class="error">%(error_password)s</span>
                    </td>
                </tr>
                <tr>
                    <td><label for="verified">Verify Password</label></td>
                    <td>
                        <input name="verified" type="password" >
                        <span class="error">%(error_verify)s</span>
                    </td>
                </tr>
                <tr>
                    <td><label for="email">Email (optional)</label></td>
                    <td>
                        <input name="email" type="text" value="%(email)s">
                        <span class="error">%(error_email)s</span>
                    </td>
                </tr>
            </table>
            <input type="submit">
        </form>


    </body>
</html>
"""


thanks = """
<!DOCTYPE html>
<html>
    <head>
        <title>User Sign-up</title>
        <style type="text/css">
            .error {
                color: red;
            }
        </style>
    </head>
    <body>
    <h1>
        User Sign-up
    </h1>

    <div>Thanks %(username)s! That's a totally valid sign up!</div>

    </body>
</html>
"""

def escape_html(s):
    return cgi.escape(s, quote = True)

USER_RE = re.compile(r"^.{1,}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{1,}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)




class MainHandler(webapp2.RequestHandler):

    def get(self, error_username="", error_password="", error_verify="", error_email="", email="", username=""):

        self.response.out.write(form %{"error_username": error_username,
                                        "error_password": error_password,
                                        "error_verify": error_verify,
                                        "error_email": error_email,
                                        "email": email,
                                        "username": username,
                                        })

    def post(self, error_username="", error_password="", error_verify="", error_email="", email="", username=""):


        have_error = False

        input_username = self.request.get('username')
        input_password = self.request.get('password')
        email = self.request.get('email')
        verified = self.request.get('verified')

        if not valid_username(input_username):
            error_username = "You don't have an identity without a handle!"
            have_error = True

        elif valid_username(input_username):
            username = input_username

        if not valid_password(input_password):
            error_password = "Speak friend and enter"
            have_error = True
        elif input_password != verified:
             error_verify = "Somebody left their typing fingers at home, didn't they..."
             have_error = True

        if not valid_email(email):
            error_email = "Something seems to be missing @here"
            have_error = True


        if have_error:
            self.response.out.write(form % {"error_username": error_username,
                                            "error_password": error_password,
                                            "error_verify": error_verify,
                                            "error_email": error_email,
                                            "email": email,
                                            "username": username,
                                            })

        else:
            self.redirect("/thanks?username=" + input_username)

class ThanksHandler(webapp2.RequestHandler):

    def get(self):
        username = self.request.get('username')

        if valid_username(username):
            self.response.out.write(thanks % {"username": username})
        else:
            self.redirect('/')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/thanks', ThanksHandler)
], debug=True)
