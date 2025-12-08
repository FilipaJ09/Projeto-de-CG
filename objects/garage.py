from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import Image
import sys, os

class Garage:
    def __init__(self):
        self.width = 10.0
        self.depth = 8.0
        self.wall_h = 3.5
        self.thickness = 0.4

    def draw_textured_cube(self, flag=True):
        """Dependendo da flag, desenha um cubo de lado 2 com ou sem textura 
            (flag = True, ou flag = False, respetivamente)"""
        if flag:
            def load_texture(path, repeat=True): 
                base_dir = os.path.dirname(__file__)
                path = os.path.join(base_dir, path)
                if not os.path.isfile(path): 
                    print(f"Aviso: Textura não encontrada: {path}")
                    return None
                
                img = Image.open(path).convert("RGBA")
                w, h = img.size 
                data = img.tobytes("raw", "RGBA", 0, -1)

                tex_id = glGenTextures(1)
                glBindTexture(GL_TEXTURE_2D, tex_id)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR) 
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT if repeat else GL_CLAMP_TO_EDGE)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT if repeat else GL_CLAMP_TO_EDGE)
                gluBuild2DMipmaps(GL_TEXTURE_2D, GL_RGBA, w, h, GL_RGBA, GL_UNSIGNED_BYTE, data)
                
                return tex_id
            texID = load_texture("garage2_texture.jpg", repeat=True)
            if texID:
                glEnable(GL_TEXTURE_2D) 
                glBindTexture(GL_TEXTURE_2D, texID)
            glEnable(GL_NORMALIZE) 
            glColor3f(1, 1, 1)
            glNormal3f(0, 1, 0)
            T = 1
            # Frente
            glBegin(GL_QUADS)
            glTexCoord2f(0.0, 0.0); glVertex3f(-0.5, -0.5,  0.5)
            glTexCoord2f(T, 0.0); glVertex3f( 0.5, -0.5,  0.5)
            glTexCoord2f(T, T); glVertex3f( 0.5, 0.5, 0.5)
            glTexCoord2f(0.0, T); glVertex3f(-0.5,  0.5, 0.5)
            glEnd()

            # Traseira
            glBegin(GL_QUADS)
            glTexCoord2f(0.0, 0.0); glVertex3f(-0.5, -0.5, -0.5)
            glTexCoord2f(T, 0.0); glVertex3f( 0.5, -0.5, -0.5)
            glTexCoord2f(T, T); glVertex3f( 0.5,  0.5, -0.5)
            glTexCoord2f(0.0, T); glVertex3f(-0.5,  0.5, -0.5)
            glEnd()

            # Esquerda
            glBegin(GL_QUADS)
            glTexCoord2f(0.0, 0.0); glVertex3f(-0.5, -0.5, -0.5)
            glTexCoord2f(T, 0.0); glVertex3f(-0.5, -0.5,  0.5)
            glTexCoord2f(T,T); glVertex3f(-0.5,  0.5,  0.5)
            glTexCoord2f(0.0,T); glVertex3f(-0.5,  0.5, -0.5)
            glEnd()

            # Direita
            glBegin(GL_QUADS)
            glTexCoord2f(0.0, 0.0); glVertex3f( 0.5, -0.5, -0.5)
            glTexCoord2f(T, 0.0); glVertex3f( 0.5, -0.5,  0.5)
            glTexCoord2f(T,T); glVertex3f( 0.5,  0.5,  0.5)
            glTexCoord2f(0.0, T); glVertex3f( 0.5,  0.5, -0.5)
            glEnd()

            # Topo
            glBegin(GL_QUADS)
            glTexCoord2f(0.0, 0.0); glVertex3f(-0.5, 0.5, -0.5)
            glTexCoord2f(T, 0.0); glVertex3f( 0.5, 0.5, -0.5)
            glTexCoord2f(T,T); glVertex3f( 0.5, 0.5, 0.5)
            glTexCoord2f(0.0, T); glVertex3f(-0.5, 0.5, 0.5)
            glEnd()

            # Fundo
            glBegin(GL_QUADS)
            glTexCoord2f(0.0, 0.0); glVertex3f(-0.5, -0.5, -0.5)
            glTexCoord2f(T, 0.0); glVertex3f( 0.5, -0.5, -0.5)
            glTexCoord2f(T,T); glVertex3f( 0.5, -0.5,  0.5)
            glTexCoord2f(0.0, T); glVertex3f(-0.5, -0.5,  0.5)
            glEnd()

            glDisable(GL_TEXTURE_2D)
        else :
            glutSolidCube(1.0)

    def draw_block(self, x, y, z, w, h, d, color):
        glPushMatrix()
        glTranslatef(x, y, z)
        glScalef(w, h, d)
        glColor3fv(color)
        # glutSolidCube(1.0)
        self.draw_textured_cube(flag=False)
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
        glPushMatrix()
        glScalef(3, 3, 3)
        white = (1.0, 1.0, 1.0)
        # -- Desenhar o Chão -- 
        self.draw_floor()

        # -- Teto --
        self.draw_block(0, self.wall_h, -self.depth/2, self.width, 0.2, self.depth, white)

        # -- Paredes (Trás e Lados) --
        self.draw_block(0, self.wall_h/2, -self.depth, self.width, self.wall_h, self.thickness, white)
        self.draw_block(-self.width/2 + self.thickness/2, self.wall_h/2, -self.depth/2, self.thickness, self.wall_h, self.depth, white)
        self.draw_block(self.width/2 - self.thickness/2, self.wall_h/2, -self.depth/2, self.thickness, self.wall_h, self.depth, white)

        # -- Fachada Frontal (Agora toda branca) --
        z_face = 0.0
        # Lado Esquerdo
        self.draw_block(-4.5, self.wall_h/2, z_face, 1.5, self.wall_h, self.thickness, white) 
        self.draw_block(-2.0, self.wall_h/2, z_face, 1.0, self.wall_h, self.thickness, white)    
        self.draw_block(-3.25, 3.0, z_face, 1.5, 1.0, self.thickness, white)        
        self.draw_block(-3.25, 0.5, z_face, 1.5, 1.0, self.thickness, white)        
        # Lado Direito
        self.draw_block(4.5, self.wall_h/2, z_face, 1.5, self.wall_h, self.thickness, white) 
        self.draw_block(2.0, self.wall_h/2, z_face, 1.0, self.wall_h, self.thickness, white)       
        self.draw_block(3.25, 3.0, z_face, 1.5, 1.0, self.thickness, white)               
        self.draw_block(3.25, 0.5, z_face, 1.5, 1.0, self.thickness, white)               
        # Placa Central
        self.draw_block(0.0, 3.25, z_face, 3.0, 1.5, self.thickness, white)

        glPopMatrix()
