from OpenGL.GL import *
from OpenGL.GLUT import *

class Garage:
    def __init__(self):
        self.width = 10.0
        self.depth = 8.0
        self.wall_h = 3.5
        self.thickness = 0.4

    def draw_block(self, x, y, z, w, h, d, color):
        glPushMatrix()
        glTranslatef(x, y, z)
        glScalef(w, h, d)
        glColor3fv(color)
        glutSolidCube(1.0)
        glPopMatrix()

    def draw_floor(self):
        # Desenha o chão 
        glDisable(GL_CULL_FACE) # Garante que se vê de qualquer lado
        glNormal3f(0.0, 1.0, 0.0)
        glColor3f(0.5, 0.5, 0.55)
        
        half_w = int(self.width / 2)
        y_floor = 0.0
        
        # Loop com inteiros para evitar buracos
        for x in range(-half_w, half_w):
            for z in range(-int(self.depth), 0):
                glBegin(GL_QUADS)
                glVertex3f(x, y_floor, z)
                glVertex3f(x + 1, y_floor, z)
                glVertex3f(x + 1, y_floor, z + 1)
                glVertex3f(x, y_floor, z + 1)
                glEnd()
        glEnable(GL_CULL_FACE)

    def draw(self):
        # -- Desenhar o Chão -- 
        self.draw_floor()

        # -- Configurar Cores --
        col_roof = (0.9, 0.9, 0.9)
        col_walls = (0.3, 0.2, 0.1)
        # Fachada
        col_orange = (0.9, 0.5, 0.1)
        col_red = (0.7, 0.2, 0.2)
        col_purple = (0.6, 0.4, 0.7)
        col_green = (0.2, 0.6, 0.3)
        col_blue = (0.3, 0.5, 0.9)

        # -- Teto --
        self.draw_block(0, self.wall_h, -self.depth/2, self.width, 0.2, self.depth, col_roof)
        
        # -- Paredes (Trás e Lados) --
        self.draw_block(0, self.wall_h/2, -self.depth, self.width, self.wall_h, self.thickness, col_walls)
        self.draw_block(-self.width/2 + self.thickness/2, self.wall_h/2, -self.depth/2, self.thickness, self.wall_h, self.depth, col_walls)
        self.draw_block(self.width/2 - self.thickness/2, self.wall_h/2, -self.depth/2, self.thickness, self.wall_h, self.depth, col_walls)

        # -- Fachada Frontal --
        z_face = 0.0
        # Lado Esquerdo
        self.draw_block(-4.5, self.wall_h/2, z_face, 1.5, self.wall_h, self.thickness, col_orange) 
        self.draw_block(-2.0, self.wall_h/2, z_face, 1.0, self.wall_h, self.thickness, col_red)    
        self.draw_block(-3.25, 3.0, z_face, 1.5, 1.0, self.thickness, col_purple)        
        self.draw_block(-3.25, 0.5, z_face, 1.5, 1.0, self.thickness, col_purple)        
        # Lado Direito
        self.draw_block(4.5, self.wall_h/2, z_face, 1.5, self.wall_h, self.thickness, (0.4, 0.2, 0.6)) 
        self.draw_block(2.0, self.wall_h/2, z_face, 1.0, self.wall_h, self.thickness, col_green)       
        self.draw_block(3.25, 3.0, z_face, 1.5, 1.0, self.thickness, col_blue)               
        self.draw_block(3.25, 0.5, z_face, 1.5, 1.0, self.thickness, col_blue)               
        # Placa Central
        self.draw_block(0.0, 3.25, z_face, 3.0, 1.5, self.thickness, (0.7, 0.7, 0.8))