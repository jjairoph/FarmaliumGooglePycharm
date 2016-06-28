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
# -*- coding: latin-1 -*-
import os
import urllib
import MySQLdb
import webapp2
import jinja2
import logging
#import pdb

#pdb.set_trace()

CLOUDSQL_PROJECT = 'pharmallium'
CLOUDSQL_INSTANCE = 'pharmallium'
LOCALSQL_INSTANCE = 'pharmallium'

#PASSWD_LOCAL = "farmalium2016"
PASSWD_LOCAL = "elpdhsqep"

DEFAULT_QUERY = ''

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def handle_404(request, response, exception):
    direccion = request.path + request.url
    template_values = {
        'mensaje0': 'Pagina no encontrada!!!',
        'mensaje1': 'Podrias volver ',
        'mensaje2': 'pero nosotros te invitamos a seguir siempre',
    }
    logging.exception(exception)
    template = JINJA_ENVIRONMENT.get_template('/templates/error.html')
    response.write(template.render(template_values))
    response.set_status(404)

def handle_500(request, response, exception):
    direccion = request.path
    url = request.url
    logging.exception(exception)
    mensage = exception
    template_values = {
        'mensaje0': 'Error en el servidor!!!',
        'mensaje1': str(mensage),
        'mensaje2': 'Error interno',
    }
    logging.exception(exception)
    template = JINJA_ENVIRONMENT.get_template('/templates/error.html')
    response.write(template.render(template_values))
    response.set_status(500)




class Resultado(webapp2.RequestHandler):
    def get(self):
        template_values = {
            'consulta': 'consulta',
            'url_linktext': 'url_linktext',
        }
        template = JINJA_ENVIRONMENT.get_template('/templates/resultado.html')
        self.response.write(template.render(template_values))

class FarmaliumRecomienda(webapp2.RequestHandler):
    def get(self):
        template_values = {
            'consulta': 'consulta',
            'url_linktext': 'url_linktext',
        }
        template = JINJA_ENVIRONMENT.get_template('/templates/index_con_resultados.html ')
        self.response.write(template.render(template_values))


class Resultado(webapp2.RequestHandler):
    def get(self):
        template_values = {
            'greetings': 'greetings',
            'url': 'url',
            'url_linktext': 'url_linktext',
        }
        template = JINJA_ENVIRONMENT.get_template('/templates/resultado.html')
        self.response.write(template.render(template_values))

class IndexConResultado(webapp2.RequestHandler):
    def get(self):
        template_values = {
            'greetings': 'greetings',
            'url': 'url',
            'url_linktext': 'url_linktext',
        }
        template = JINJA_ENVIRONMENT.get_template('/templates/index_con_resultados.html')
        self.response.write(template.render(template_values))


class MainPage(webapp2.RequestHandler):
    def get(self):
        #self.response.headers['Content-Type'] = 'text/plain'
        consulta = self.request.get('consulta', DEFAULT_QUERY)

        # When running on Google App Engine, use the special unix socket
        # to connect to Cloud SQL.
        # if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
        #     db = MySQLdb.connect(
        #         unix_socket='/cloudsql/pharmallium:us-central1:pharmallium'.format(
        #             CLOUDSQL_PROJECT,
        #             CLOUDSQL_INSTANCE),
        #         user='conexion', passwd="elpdhsqep", db=CLOUDSQL_INSTANCE)
        # # When running locally, you can either connect to a local running
        # # MySQL instance, or connect to your Cloud SQL instance over TCP.
        # else:
        #     db = MySQLdb.connect(host='localhost', user='root', passwd=PASSWD_LOCAL, db=LOCALSQL_INSTANCE )
        #
        # cursor = db.cursor()
        # cursor.execute('select distinct producto_nuevo from pharmallium.invima_depu order by 1')

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
        #self.response.write('es la principal')


class Consulta(webapp2.RequestHandler):
     #def post(self):
     def get(self):
         consulta = self.request.GET['med']
         elquery = str(consulta)
         elementos = []
         elementos = elquery.split()
         if len(elementos) > 0:
            medicamento = elementos[0]
            # We set the same parent key on the 'Greeting' to ensure each
            # Greeting is in the same entity group. Queries across the
            # single entity group will be consistent. However, the write
            # rate to a single entity group should be limited to
            # ~1/second.
            #consulta = self.request.POST.items
            #query_params = {'consulta': consulta}
            #self.redirect('/?' + urllib.urlencode(query_params))
            #self.response.write('es la consulta')

            if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
                    db = MySQLdb.connect(
                        unix_socket='/cloudsql/pharmallium:us-central1:db'.format(
                        CLOUDSQL_PROJECT,
                        CLOUDSQL_INSTANCE),
                    user='root', passwd="chelin1974", db=CLOUDSQL_INSTANCE)
            # When running locally, you can either connect to a local running
            # MySQL instance, or connect to your Cloud SQL instance over TCP.
            else:
                    db = MySQLdb.connect(host='localhost', user='root', passwd=PASSWD_LOCAL, db=LOCALSQL_INSTANCE)

            '#Validar que se enviaron parametros de consulta'
            medicamento = '%' + medicamento + '%'
            del elementos[0]  #Borrar nombre medicamento
            '#No mostrar muestras medicas ni inactivos'
            estadoActivo = 'Activo'
            muestraMedica = 'No'
            filtro = '%'
            if len(elementos) > 0:
                for parametros in elementos:
                    parametros = '%' + parametros + '%'
                    filtro = filtro + parametros

            cursor = db.cursor()
            query = 'Select distinct a.producto_nuevo, a.descripcion_atc_unido From pharmallium.invima_depu as a inner join ' \
                    '(SELECT distinct descripcion_atc_unido FROM pharmallium.invima_depu where producto_nuevo like %s ) as b on a.descripcion_atc_unido = b.descripcion_atc_unido' \
                    ' and producto_nuevo like %s order by 1'
                    #' and a.estado_cum = %s and muestra_medica = %s ' \

            #cursor.execute(query, (medicamento, estadoActivo, muestraMedica, filtro,))
            cursor.execute(query, (medicamento, filtro,))
            my_list = []
            #for r in cursor.fetchmany(200):
            my_list = cursor.fetchmany(200)

            #data = [[[1, 2, 3, 4], [2, 4, 5]], ["abc", "def"]]
            #my_list = data

            #self.response.write('{}\n'.format(r))

            template_values = {
                'consulta': consulta,
                'url_linktext': 'url_linktext',
                'my_list': my_list
            }
            template = JINJA_ENVIRONMENT.get_template('/templates/index.html')
            self.response.write(template.render(template_values))
            #self.response.write(template.render(my_list))
            # [END guestbook]
         else:
             '#Error no consulta nada'


# [START app]
app = webapp2.WSGIApplication([('/', MainPage), ('/index.html', MainPage),   ('/consulta*', Consulta), (r'/resultado.html', Resultado), (r'/index_con_resultados.html', FarmaliumRecomienda)], debug=True)
app.error_handlers[404] = handle_404
app.error_handlers[500] = handle_500

#app = webapp2.WSGIApplication([(r'/', HomeHandler),  (r'/products', ProductListHandler), (r'/products/(\d+)', ProductHandler),])

# [END app]