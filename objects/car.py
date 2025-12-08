from OpenGL.GL import *
from OpenGL.GLUT import *

#import pywavefront #biblioteca importada para conseguir usar o carro criado no blender no python
#from pywavefront.visualization import draw
import numpy as np
import math
import sys, os
from objects.obj_loader import OBJModel

#função para calcular os pontos de pivô das partes móveis do carro
def calculate_pivot_points(obj):
    verts = np.array(obj.vertices).reshape(-1, 3) #converter a lista de vértices em um array numpy para facilitar os cálculos
    min_v = verts.min(axis=0) #encontrar o ponto mínimo em cada eixo
    max_v = verts.max(axis=0) #encontrar o ponto máximo em cada eixo
    center = (min_v + max_v) / 2 #calcular o centro do objeto
    return min_v, max_v, center

class Car:

    #função para inicializar as componentes do carro
    def __init__(self):
        base_dir = os.path.dirname(__file__) 
        models_dir = os.path.join(base_dir, "models")

        #componentes do carro
        """ self.body = pywavefront.Wavefront("models/Body.obj")            #corpo principal do carro
        self.left_door = pywavefront.Wavefront("models/Left_Door.obj")      #porta esquerda do carro
        self.right_door = pywavefront.Wavefront("models/Right_Door.obj")    #porta direira do carro
        self.back_wheels = pywavefront.Wavefront("models/Wheels_Bk.obj")    #rodas traseiras do carro
        self.front_wheels = pywavefront.Wavefront("models/Wheels_Ft.obj")   #rodas dianteiras do carro
        self.ste_wheel = pywavefront.Wavefront("models/Steering_Wheel.obj") #volante do carro 
        """
        self.body = OBJModel(os.path.join(models_dir, "Body.obj"))
        self.left_door = OBJModel(os.path.join(models_dir, "Left_Door.obj"))
        self.right_door = OBJModel(os.path.join(models_dir, "Right_Door.obj"))
        self.back_wheels = OBJModel(os.path.join(models_dir, "Wheels_Bk.obj"))
        self.front_wheels = OBJModel(os.path.join(models_dir, "Wheels_Ft.obj"))
        self.ste_wheel = OBJModel(os.path.join(models_dir, "Steering_Wheel.obj"))
        
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
        self.left_door_pivot = self.left_door_max          #pivô da porta esquerda -->como min porque vai estar no eixo mais extremo
        self.right_door_pivot = self.right_door_max        #pivô da porta direita -->como max porque vai estar no eixo mais extremo
        self.back_wheels_pivot = self.back_wheels_center   #pivô das rodas traseiras --> rodas giram em torno do seu centro
        self.front_wheels_pivot = self.front_wheels_center #pivô das rodas dianteiras --> rodas giram em torno do seu centro
        self.ste_wheel_pivot = self.ste_wheel_center       #pivô do volante --> volante gira em torno do seu centro

        #posição e movimento do carro
        self.x = 0.0          #posição X do carro
        self.z = 0.0          #posição z do carro  
        self.speed = 0.1      #velocidade do carro
        self.direction = 0.0  #direção do carro em graus (estar em 0 graus faz o carro andar em frente)

    #função para abrir/fechar portas do carro
    def trigger(self, side ="left"):
        if side =="left":
            if self.left_door_angle < 0 :
                self.left_door_angle = 0
            else :
                self.left_door_angle = -50
        elif side =="right":
            if self.right_door_angle > 0 :
                self.right_door_angle = 0
            else :
                self.right_door_angle = 50

    #função para desenhar a porta esquerda do carro
    def draw_left_door(self):
        glPushMatrix()
        #glTranslatef(*self.left_door_pivot)      # mover para pivot
        glTranslatef(0.55, -0.68,0.9)
        glRotatef(self.left_door_angle, 0, 1, 0) # rodar no eixo Y (porta balança para fora)
        #glTranslatef(*(-self.left_door_pivot))   # voltar ao sítio
        glTranslatef(-0.55, 0.68,-0.9)
        glTranslatef(0.62, 0.0,0.227) #para posicionar no sítio certo
        #draw(self.left_door)
        self.left_door.draw()
        glPopMatrix()

    #função para desenhar a porta direita do carro
    def draw_right_door(self):
        glPushMatrix()
        glTranslatef(-0.55, -0.68,0.9)
        # glTranslatef(*self.right_door_pivot)      # mover para pivot
        glRotatef(self.right_door_angle, 0, 1, 0) # rodar no eixo Y (porta balança para fora)
        # glTranslatef(*(-self.right_door_pivot))   # voltar ao sítio
        glTranslatef(0.55, 0.68,-0.9)
        glTranslatef(-0.62, 0.0,0.227) #para posicionar no sítio certo
        #draw(self.right_door)
        self.right_door.draw()
        glPopMatrix()

    #função para desenhar as rodas traseiras do carro ---> com movimento mais lento atrás
    def draw_back_wheels(self):
        glPushMatrix()
        glTranslatef(*self.back_wheels_pivot)      # mover para pivot
        glRotatef(self.back_wheels_angle, 1, 0, 0) # rodar no eixo X (rodas giram para andar)
        glTranslatef(*(-self.back_wheels_pivot))   # voltar ao sítio
        glTranslatef(0.0,-0.5,-1.0)
        #draw(self.back_wheels)   # desenhar pneus
        self.back_wheels.draw()
        glPopMatrix()

    #função para desenhar as rodas dianteiras do carro ---> com movimento mais rápido do que as rodas de trás
    def draw_front_wheels(self):
        glPushMatrix()
        glTranslatef(*self.front_wheels_pivot)      # mover para pivot
        glRotatef(self.front_wheels_angle, 1, 0, 0) # rodar no eixo X (rodas giram para andar)
        glTranslatef(*(-self.front_wheels_pivot))   # voltar ao sítio
        glTranslatef(0.0,-0.5,1.25)
        #draw(self.front_wheels)   # desenhar pneus
        self.front_wheels.draw()
        glPopMatrix() 

    #função para desenhar o volante do carro 
    def draw_ste_wheel(self):
        glPushMatrix()
        glTranslatef(-0.33,-0.63,0.9)
        # glTranslatef(*self.ste_wheel_pivot)      # mover para pivot
        glRotatef(self.ste_wheel_angle, 0, 0, 1) # rodar no eixo Y (volante gira para virar o carro)
        # glTranslatef(*(-self.ste_wheel_pivot))   # voltar ao sítio
        glTranslatef(0.33,0.63,-0.9)
        glTranslatef(0.27, 0.07,0.47)
        #draw(self.ste_wheel)   # desenhar pneus
        self.ste_wheel.draw()
        glPopMatrix() 

    def ste_wheel_turn(self, forward=True):
        turn_angle = 5  #ângulo de viragem do volante por chamada da função

        if forward:
            self.ste_wheel_angle += turn_angle
        else:
            self.ste_wheel_angle -= turn_angle

     #função para animar a rotação das rodas do carro
    def car_move(self, forward=True):
        direction_multiplier = 1 if forward else -1 #definir o sentido do movimento (frente ou trás)

        #atualizar a posição do carro 
        self.x += math.sin(math.radians(self.direction)) * self.speed * direction_multiplier #atualizar a posição X do carro com base na direção e velocidade
        self.z += math.cos(math.radians(self.direction)) * self.speed * direction_multiplier #atualizar a posição Z do carro com base na direção e velocidade
        
        #velocidade de rotação das rodas
        bk_rot = 0.025 * self.speed    #velocidade das rodas traseiras (mais lentas)
        ft_rot = 0.05 * self.speed    #velocidade das rodas dianteiras (mais rápidas)

        #atualizar os ângulos de rotação das rodas
        self.back_wheels_angle += bk_rot * direction_multiplier  #atualizar o ângulo das rodas traseiras
        self.front_wheels_angle += ft_rot * direction_multiplier #atualizar o ângulo das rodas dianteiras


    #função para desenhar o carro
    def draw_car(self):
        glPushMatrix()
        glTranslatef(self.x, 0.0, self.z)  #mover o carro para a sua posição atual
        glRotatef(self.direction, 0, 1, 0) #rodar
        glColor3f(1.0, 1.0, 1.0)
        self.body.draw()
        #draw(self.body)  #desenhar corpo do carro
      
        #desenhar portas 
        self.draw_left_door()
        self.draw_right_door()
       

        #desenhar rodas
        self.draw_back_wheels()
        self.draw_front_wheels()

        #desenhar volante
        self.draw_ste_wheel()
        glPopMatrix()

    
