from OpenGL.GL import *
from OpenGL.GLUT import *

import pywavefront #biblioteca importada para conseguir usar o carro criado no blender no python
from pywavefront.visualization import draw
import numpy as np

#função para calcular os pontos de pivô das partes móveis do carro
def calculate_pivot_points(obj):
    verts = np.array(obj.vertices).reshape(-1, 3) #converter a lista de vértices em um array numpy para facilitar os cálculos
    min_v = verts.min(axis=0) #encontrar o ponto mínimo em cada eixo
    max_v = verts.max(axis=0) #encontrar o ponto máximo em cada eixo
    center = (min_v + max_v) / 2 #calcular o centro do objeto
    return min_v, max_v, center

class car:

    #função para inicializar as componentes do carro
    def __init__(self):
        
        #componentes do carro
        self.body = pywavefront.Wavefront("models/Body.obj")                #corpo principal do carro
        self.left_door = pywavefront.Wavefront("models/Left_Door.obj")      #porta esquerda do carro
        self.right_door = pywavefront.Wavefront("models/Right_Door.obj")    #porta direira do carro
        self.back_wheels = pywavefront.Wavefront("models/Wheels_Bk.obj")    #rodas traseiras do carro
        self.front_wheels = pywavefront.Wavefront("models/Wheels_Ft.obj")   #rodas dianteiras do carro
        self.ste_wheel = pywavefront.Wavefront("models/Steering_Wheel.obj") #volante do carro ----> importante
        
        #ângulos iniciais das partes móveis do carro
        self.left_door_angle = 0       #ângulo da porta esquerda
        self.right_door_angle = 0      #ângulo da porta direita
        self.back_wheels_angle = 0     #ângulo das rodas traseiras
        self.front_wheels_angle = 0    #ângulo das rodas dianteiras
        self.ste_wheel_angle = 0       #ângulo do volante

        #calcular bounding boxes das partes móveis do carro para definir os pontos de pivô
        self.left_door_min, self.left_door_max, self.left_door_center = calculate_pivot_points(self.left_door)              #bounding boxes de pivô da porta esquerda
        self.right_door_min, self.right_door_max, self.right_door_center = calculate_pivot_points(self.right_door)          #bounding boxes de pivô da porta direita
        self.back_wheels_min, self.back_wheels_max, self.back_wheels_center = calculate_pivot_points(self.back_wheels)      #bounding boxes de pivô das rodas traseiras
        self.front_wheels_min, self.front_wheels_max, self.front_wheels_center = calculate_pivot_points(self.front_wheels)  #bounding boxes de pivô das rodas dianteiras
        self.ste_wheel_min, self.ste_wheel_max, self.ste_wheel_center = calculate_pivot_points(self.ste_wheel)              #bounding boxes de pivô do volante

        #definir os pivôs das partes móveis do carro
        self.left_door_pivot = self.left_door_min          #pivô da porta esquerda -->como min porque vai estar no eixo mais extremo
        self.right_door_pivot = self.right_door_max        #pivô da porta direita -->como max porque vai estar no eixo mais extremo
        self.back_wheels_pivot = self.back_wheels_center   #pivô das rodas traseiras --> rodas giram em torno do seu centro
        self.front_wheels_pivot = self.front_wheels_center #pivô das rodas dianteiras --> rodas giram em torno do seu centro
        self.ste_wheel_pivot = self.ste_wheel_center       #pivô do volante --> volante gira em torno do seu centro


    #função para desenhar a porta esquerda do carro
    def draw_left_door(self):
        glPushMatrix()
        glTranslatef(*self.left_door_pivot)      # mover para pivot
        glRotatef(self.left_door_angle, 0, 1, 0) # rodar no eixo Y (porta balança para fora)
        glTranslatef(*(-self.left_door_pivot))   # voltar ao sítio
        draw(self.left_door)
        glPopMatrix()

    #função para desenhar a porta direita do carro
    def draw_right_door(self):
        glPushMatrix()
        glTranslatef(*self.right_door_pivot)      # mover para pivot
        glRotatef(self.right_door_angle, 0, 1, 0) # rodar no eixo Y (porta balança para fora)
        glTranslatef(*(-self.right_door_pivot))   # voltar ao sítio
        draw(self.right_door)
        glPopMatrix()

    #função para desenhar as rodas traseiras do carro ---> com movimento mais lento atrás
    def draw_back_wheels(self):
        glPushMatrix()
        glTranslate(*self.back_wheels_pivot)      # mover para pivot
        glRotatef(self.back_wheels_angle, 0, 0, 1) # rodar no eixo X (rodas giram para andar)
        glTranslate(*(-self.back_wheels_pivot))   # voltar ao sítio
        draw(self.back_wheels)   # desenhar pneus
        glPopMatrix()

    #função para desenhar as rodas dianteiras do carro ---> com movimento mais rápido do que as rodas de trás
    def draw_front_wheels(self):
        pass 

    #função para desenhar o volante do carro 
    def draw_ste_wheel(self):
        pass

    #função para desenhar o carro
    def draw(self):
        #desenhar corpo do carro
        draw(self.body)
        draw(self.body_bumper)
        draw(self.body_exten)

        #portas e bagageira 
        draw_left_door(self)
        draw_right_door(self)
        draw(self.lug_compart)

        #rodas e pneus
        draw_back_wheels(self)
        draw_front_wheels(self)

        #desenhar o interior e acessórios do carro
        draw(self.ste_wheel)
        draw(self.accessories)
        draw(self.interior)
        draw(self.engine)
        draw(self.suspension)
        draw(self.glass)
         

         
         
         
         
         
        
