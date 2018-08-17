#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import re
import codecs

from docx import Document
from random import shuffle

class FarabeufProcesser:

    def __init__(self,
                 location='data/Farabeuf Salvador Elizondo Obra completa.docx',
                 frag_regex='Fragmento ?\d{1,}',
                 read=True,
                 fragmentos=None,
                 fragment_indices=None,
                 header=False):
        self.header = header
        self.frag_regex = re.compile(frag_regex)
        if read:
            self.read_doc(location)
        else:
            self.fragmentos = fragmentos
            self.indices = list(range(len(self.fragmentos) + 1)[1:])
        if fragment_indices is not None:
            with codecs.open(fragment_indices, 'r') as f:
                self.indices = [int(n) for n in f]


    def read_doc(self, location):
        """
        Lee y pre-procesa un documento dado entre fragmentos.
        Regresa una lista de fragmentos y una lista de sus índices empezando por 1.
        """
        doc = Document(location)
        paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
        paragraphs = '**'.join(paragraphs)

        # División por fragmentos
        fragmentos = [p.strip() for p in self.frag_regex.split(paragraphs)
                      if p.strip()]

        if self.header:
            self.fragmentos = fragmentos[1:]
        else:
            self.fragmentos = fragmentos
        self.indices = list(range(len(self.fragmentos) + 1)[1:])

    def shuffle_indices(self):
        """
        Permuta aleatoriamente los fragmentos
        """
        shuffle(self.indices)

    def query_fragment(self, n):
        """
        Consulta de fragmentos
        """
        assert n > 0 and n <= len(self.fragmentos)
        return self.fragmentos[n - 1]

    def join_doc(self, header='', tail=''):
        """
        Junta los fragmentos en el orden indicado por los índices y
        separándolos por sep.
        """
        joined = header
        for i in self.indices:
            joined += '<p><p>'
            joined += self.query_fragment(i).replace('**', '<p>')
        joined += tail
        return joined
