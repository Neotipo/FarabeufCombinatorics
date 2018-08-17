#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

from flask import Flask, request, render_template, redirect
from utils.text_utils import FarabeufProcesser

app = Flask(__name__)

farabeuf_general_processer = FarabeufProcesser()
farabeuf_options = {
    'todo': (farabeuf_general_processer,
             '<i>FARABEUF</i>'),
    'enfermera': (FarabeufProcesser(fragment_indices='data/story1.txt',
                                    read=False,
                                    fragmentos=farabeuf_general_processer.fragmentos),
                  'Story of <i>Farabeuf</i> and the nurse'),
    'dr_farabeuf_1': (FarabeufProcesser(fragment_indices='data/story2.txt', read=False,
                                    fragmentos=farabeuf_general_processer.fragmentos),
                      'Story of the lovers'),
    'dr_farabeuf_2': (FarabeufProcesser(fragment_indices='data/story3.txt', read=False,
                                        fragmentos=farabeuf_general_processer.fragmentos),
                      'Story of a sacrifice'),
    'dr_farabeuf_3': (FarabeufProcesser(fragment_indices='data/no_plot.txt', read=False,
                                        fragmentos=farabeuf_general_processer.fragmentos),
                      '<i>Farabeuf</i> without plot')
}

bastardo_frag_regex = '\d+\*\*'
bastardo_pl = FarabeufProcesser(location='data/Bastardo-Planteamiento.docx',
                                frag_regex=bastardo_frag_regex)
bastardo_nu = FarabeufProcesser(location='data/Bastardo-Nudo.docx',
                                frag_regex=bastardo_frag_regex)
bastardo_de = FarabeufProcesser(location='data/Bastardo-Desenlace.docx',
                                frag_regex=bastardo_frag_regex)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html'), 200

@app.route('/iterate', methods=['POST', 'GET'])
def iterate():
    if request.method != 'POST':
        return render_template('index.html'), 200
    else:
        try:
            option = request.form['user_selection']
            fp, title = farabeuf_options[option]
            fp.shuffle_indices()
            header = '''
            <!doctype html>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <h1>{}</h1>
            '''
            header = header.format(title)
            header += '''
            <button onclick="myFunction()">Iterar de nuevo</button>
            <script>
            function myFunction() {
            location.reload();
            }
            </script>
            <p>
            <form method="GET" action="/" enctype=multipart/form-data>
            <button type="submit">Regresar al inicio</button><br>
            </form>
            '''
            output = fp.join_doc(header=header)
            return output, 200
        except:
            return 'L\'erreur', 400

@app.route('/bastardo', methods=['GET'])
def bastardo():
    try:
        bastardo_pl.shuffle_indices()
        bastardo_nu.shuffle_indices()
        bastardo_de.shuffle_indices()
        header = '''
        <!doctype html>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <h1><i>Bastardo</i></h1>
        <i>David Núñez</i>
        <p>
        '''
        header += '''
        <button onclick="myFunction()">Iterar de nuevo</button>
        <script>
        function myFunction() {
        location.reload();
        }
        </script>
        '''
        output = bastardo_pl.join_doc(header=header)
        output = bastardo_nu.join_doc(header=output)
        output = bastardo_de.join_doc(header=output)
        return output, 200
    except:
        return 'L\'erreur', 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
