# Ficheiro para manipulação dos elementos extra
# Elementos existentes: 
# - GirlTrio: Três figuras com placa de apresentação do projeto
# - BancoJardim: Banco de jardim
# - CandeeiroRua: Candeeiro de rua
# - SetaGaragem: Seta a apontar para a garagem
# - Arvore: Árvore

import math
import ctypes
import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys, os
from objects.obj_loader import OBJModel

# Classe para manipular os elementos extra
class Extra_elem:
    
    def __init__(self, filename="Arvore.obj"):
        """Cria uma instância da classe Extra_elem que recebe um path de
         ficheiro e faz load da cena com os objetos contidos nesse ficheiro"""
        base_dir = os.path.dirname(__file__)   # pasta onde está extra_elem.py
        filename = os.path.join(base_dir, filename)

        if not os.path.isfile(filename):
            print("File not found:", filename)
            sys.exit(1)
            
        # Load do objeto
        self.scene = OBJModel(filename)
    
    def draw(self, location=(0,0,0), scale= (1,1,1),angle = 0, rotation = (0,1,0)):
        """Recebe a informação necessária do objeto que se pretende e desenha-o na cena do OpenGL"""
        glPushMatrix()
        glTranslatef(*location)
        glRotatef(angle, *rotation)
        glScalef(*scale)
        glColor3f(1.0, 1.0, 1.0)
        # Desenha o objeto
        self.scene.draw()
        glPopMatrix()
