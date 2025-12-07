from OpenGL.GL import *
from OpenGL.GLUT import *

import pywavefront #biblioteca importada para passar o carro criado no blender para o 
from pywavefront.visualization import draw


class car:

    #função para inicializar as componentes do carro
     def __init__(self):
         #componentes que fazem do corpo do carro --- a ser importadas porque foram feitas com o blender
         self.body = pywavefront.Wavefront("models/Body.obj")
         self.body_bumper = pywavefront.Wavefront("models/Body_Bumper_Under.obj")
         self.body_exten = pywavefront.Wavefront("models/Body_Extensions.obj")
         
         #portas do carro
         self.left_door = pywavefront.Wavefront("models/Left_Door.obj") #porta esquerda do carro
         self.right_door = pywavefront.Wavefront("models/Right_Door.obj") #porta direira do carro
         self.lug_compart = pywavefront.Wavefront("models/lug_compart.obj") #bagageira
         
         #rodas do carro e jantes
         self.back_wheels = pywavefront.Wavefront("models/Wheels_Bk.obj") #rodas traseiras do carro
         self.back_tires = pywavefront.Wavefront("models/Tires_Bk.obj") #jantes das rodas traseiras
         self.front_wheels = pywavefront.Wavefront("models/Wheels_Ft.obj") #rodas dianteiras do carro
         self.front_tires = pywavefront.Wavefront("models/Tires_Ft.obj") #jantes dianteiras do carro

         #Acessórios do carro
         self.ste_wheel = pywavefront.Wavefront("models/Steering_Wheel.obj") #volante do carro ----> importante
         self.accessories = pywavefront.Wavefront("models/Interior_Acessorios.obj") #outros acessórios do carro
         self.interior = pywavefront.Wavefront("models/Interior_Upholstered.obj") #interior do carro
         self.engine = pywavefront.Wavefront("models/Engine.obj") #interior do carro
         self.suspension = pywavefront.Wavefront("models/Exhaust_Suspensao.obj") #eixo do carro
         self.glass = pywavefront.Wavefront("models/Glass.obj") #vidro do carro


         #
         self.left_door_angle = 0
         self.right_door_angle = 0
         self.lug_compart_angle = 0
         self.back_wheels_angle = 0
         self.back_tires_angle = 0
         self.front_wheels_angle = 0
         
         

    #função para desenhar o carro
    def draw(self):
        #corpo do carro
        draw(self.body)
        draw(self.body_bumper)
        draw(self.body_exten)

        #portas e bagageira 
        draw(self.left_door)
        draw(self.right_door)
        draw(self.lug_compart)

        #rodas e pneus
        draw(self.back_wheels)
        draw(self.back_tires)
        draw(self.front_wheels)
        draw(self.front_tires)

        #interior e acessórios do carro
        draw(self.ste_wheel)
        draw(self.accessories)
        draw(self.interior)
        draw(self.engine)
        draw(self.suspension)
        draw(self.glass)
         

         
         
         
         
         
        
