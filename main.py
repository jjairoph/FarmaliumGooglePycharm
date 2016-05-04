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
import os
import urllib
import MySQLdb
import webapp2
import jinja2

CLOUDSQL_PROJECT = 'farmalium'
CLOUDSQL_INSTANCE = 'farmalium_latin1'

DEFAULT_QUERY = ''

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        #self.response.headers['Content-Type'] = 'text/plain'
        consulta = self.request.get('consulta', DEFAULT_QUERY)

        # When running on Google App Engine, use the special unix socket
        # to connect to Cloud SQL.
        if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
            db = MySQLdb.connect(
                unix_socket='/cloudsql/farmalium:us-central1:farmalium'.format(
                    CLOUDSQL_PROJECT,
                    CLOUDSQL_INSTANCE),
                user='root', passwd="elpdhsqep", db="farmalium_latin1")
        # When running locally, you can either connect to a local running
        # MySQL instance, or connect to your Cloud SQL instance over TCP.
        else:
            db = MySQLdb.connect(host='localhost', user='root', passwd="farmalium2016", db="farmalium_latin1" )

        cursor = db.cursor()
        cursor.execute('select distinct producto from invimacompletaexcel order by 1')

        #Muestra el resultado de la CONSULTA
        #for r in cursor.fetchall():
        #for r in cursor.fetchmany(20):
        #    self.response.write('{}\n'.format(r))

        user = 'Nombre usuario'
        greetings = 'Hola, Buenas tardes'
        url = 'http://meristation.com'
        url_linktext = 'Link a merisation'

        template_values = {
            'greetings': greetings,
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('/templates/index.html')
        self.response.write(template.render(template_values))


class Consulta(webapp2.RequestHandler):
     def post(self):
         # We set the same parent key on the 'Greeting' to ensure each
         # Greeting is in the same entity group. Queries across the
         # single entity group will be consistent. However, the write
         # rate to a single entity group should be limited to
         # ~1/second.
         consulta = self.request.POST.items
         query_params = {'consulta': consulta}
         self.redirect('/?' + urllib.urlencode(query_params))
         # [END guestbook]


# [START app]
app = webapp2.WSGIApplication([('/', MainPage),    ('/*', Consulta)], debug=True)
app = webapp2.WSGIApplication([(r'/', HomeHandler),  (r'/products', ProductListHandler), (r'/products/(\d+)', ProductHandler),
])

# [END app]