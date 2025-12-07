# Ficheiro para manipulação dos elementos extra
# Elementos existentes: 
# - GirlTrio: Três figuras com placa de apresentação do projeto
# - BancoJardim: Banco de jardim
# - CandeeiroRua: Candeeiro de rua
# - SetaGaragem: Seta a apontar para a garagem
# - Arvore: Árvore

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys, os
import pywavefront # é necessário instalar esta biblioteca para correr corretamente o programa
from pywavefront.obj import ObjParser

# Classe para manipular os elementos extra
class Extra_elem:
    
    def __init__(self, filename="ElementosExtra.obj"):
        """Cria uma instância da classe Extra_elem que recebe um path de
         ficheiro e faz load da cena com os objetos contidos nesse ficheiro"""
        base_dir = os.path.dirname(__file__)   # pasta onde está extra_elem.py
        filename = os.path.join(base_dir, filename)

        # if not os.path.isfile(filename):
        #     print("File not found:", filename)
        #     sys.exit(1)
        # Load 
        self.scene = pywavefront.Wavefront(filename, collect_faces=False)

    def get_obj_list(self):
        """Retorna a lista de nomes dos objetos disponíveis no ficheiro e possíveis de desenhar"""
        obj_list = []
        for name, mesh in self.scene.meshes.items():
            obj_list.append(name)
        return obj_list
    
    def draw_object(self, obj_name="Arvore", location=(0,0,0), scale= (1,1,1),angle = 0, rotation = (0,1,0)):
        """Recebe a informação necessária do objeto que se pretende e desenha-o na cena do OpenGL"""
        glPushMatrix()
        glTranslatef(*location)
        glRotatef(angle, *rotation)
        glScalef(*scale)
        #self.scene.meshes[obj_name].draw()
        mesh = self.scene.meshes[obj_name]
        for material in mesh.materials:
            glEnableClientState(GL_VERTEX_ARRAY)
            glVertexPointer(3, GL_FLOAT, 0, material.vertices)
            glDrawArrays(GL_TRIANGLES, 0, len(material.vertices)//3)
            glDisableClientState(GL_VERTEX_ARRAY)
        glPopMatrix()