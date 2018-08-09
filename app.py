#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

from flask import Flask, request, render_template
from utils.text_utils import FarabeufProcesser

app = Flask(__name__)

options = {
    'todo': FarabeufProcesser(),
    'dr_farabeuf_1': FarabeufProcesser(location='data/FRAGMENTOS DOCTOR FARABEUF.docx'),
    'dr_farabeuf_2': FarabeufProcesser(location='data/Fragmentos Doctor.docx'),
    'enfermera': FarabeufProcesser(location='data/FRAGMENTOS ENFERMERA.docx')
}

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html'), 200

@app.route('/iterate', methods=['POST'])
def iterate():
    # try:
    option = request.form['user_selection']
    fp = options[option]
    fp.shuffle_indices()
    header = '<h1>Fragmentos de <i>Farabeuf</i></h1>'
    output = fp.join_doc(header=header)
    return output, 200
    # except:
    #     return 'L\'erreur', 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
