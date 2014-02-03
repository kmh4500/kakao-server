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
import cgi
import datetime
import webapp2

from google.appengine.ext import ndb
from google.appengine.api import users

guestbook_key = ndb.Key('Guestbook', 'default_guestbook')

class Message(ndb.Model):
  user_id = ndb.IntegerProperty()
  content = ndb.TextProperty()
  room_id = ndb.IntegerProperty()
  date = ndb.DateTimeProperty(auto_now_add=True)


class MainPage(webapp2.RequestHandler):
  def get(self):
    self.response.out.write('<html><body><form action="/messages" method="get">' +
   'Room ID: <input type="text" name="room_id"><br>' +
   '<input type="submit" value="Submit">' +
   '</form> ')
    self.response.out.write('<form action="/messages" method="post">' +
   'User ID: <input type="text" name="user_id"><br>' +
   'Content: <input type="text" name="content"><br>' +
   'Room ID: <input type="text" name="room_id"><br>' +
   '<input type="submit" value="Submit">' +
   '</form> </body></html>')


class Messages(webapp2.RequestHandler):
  def post(self):
    user_id = self.request.get('user_id')
    self.response.out.write(user_id)
    self.response.out.write('<br>')
    
    content = self.request.get('content')
    self.response.out.write(content)
    self.response.out.write('<br>')
    
    room_id = self.request.get('room_id')
    self.response.out.write(room_id)
    self.response.out.write('<br>')

    message = Message()
    message.user_id = int(user_id)
    message.content = content
    message.room_id = int(room_id)
    message.put()

  def get(self):
    room_id = int(self.request.get('room_id'))
    messages = Message.query(Message.room_id == room_id).fetch(100);
    output = ''
    for message in messages:
      output += str(message.user_id) + '\\' + message.content + '\\' + str(message.room_id) + ','
    self.response.out.write(output)


app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/messages', Messages)
], debug=True)
