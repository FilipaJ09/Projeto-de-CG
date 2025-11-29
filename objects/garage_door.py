from OpenGL.GL import *
from OpenGL.GLUT import *

class Door:
    def __init__(self):
        self.height = 0.0
        self.state = 0          # 0 = Fechada, 1 = A subir, 2 = Aberta, 3 = A descer
        self.max_height= 2.2
        self.speed = 0.05

    def draw_block(self, x, y, z, w, h, d, color):
        # Função auxiliar para desenhar cubos
        glPushMatrix()
        glTranslatef(x, y, z)
        glScalef(w, h, d)
        glColor3fv(color)
        glutSolidCube(1.0)
        glPopMatrix()
    
    def update(self):
        # Atualizar a animação
        if self.state == 1: # Abrir
            self.height += self.speed
            if self.height >= self.max_height:
                self.height = self.max_height
                self.state = 2 # Aberta
        elif self.state == 3: # Fechar
            self.height -= self.speed
            if self.height <= 0.0:
                self.height = 0.0
                self.state = 0 # Fechada
        #returna true se houver animação a acontecer
        return self.state ==1 or self.state ==3
    
    def trigger(self):
        #abrir e fechar a porta
        if self.state == 0: self.state = 1
        elif self.state == 2: self.state = 3

    def draw(self):
        glPushMatrix()
        glTranslatef(0.0, self.height, -0.6)
        glTranslatef(0.0, 1.25, 0.0) 
        # Desenha a base da porta
        self.draw_block(0.0, 0.0, 0.0, 3.2, 2.5, 0.1, (0.9, 0.9, 0.95))

        # Desenha as riscas horizontais
        for i in range(5):
            y_line = -1.0 + (i * 0.5)
            self.draw_block(0.0, y_line, 0.05, 3.0, 0.05, 0.1, (0.5, 0.5, 0.6))

        glPopMatrix()