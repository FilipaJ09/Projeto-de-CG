import sys
import math
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# --- Importar objetos ---
from objects.garage import Garage
from objects.garage_door import Door

# --- Variaveis globais ---
my_garage = None
my_door = None

# Câmara
cam_x, cam_y, cam_z = 0.0, 6.0, 20.0
cam_yaw = 180.0 
CAM_SPEED = 0.5
ROT_SPEED = 3.0

def init():
    # Configurações globais (Luzes, Cores, Depth)
    glClearColor(0.05, 0.05, 0.1, 1.0) # Noite
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
    glEnable(GL_NORMALIZE) 
    
    # LUZ 0: Exterior 
    """glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, [10.0, 20.0, 20.0, 1.0])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.4, 0.4, 0.4, 1.0]) 
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.7, 0.7, 0.7, 1.0])"""
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, [10.0, 20.0, 20.0, 1.0])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.1, 0.1, 0.15, 1.0]) 
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.1, 0.1, 0.2, 1.0])

    # LUZ 1: Interior Forte
    """glEnable(GL_LIGHT1)
    glLightfv(GL_LIGHT1, GL_POSITION, [0.0, 3.5, -4.0, 1.0]) 
    glLightfv(GL_LIGHT1, GL_DIFFUSE, [2.0, 1.2, 0.0, 1.0])   
    glLightfv(GL_LIGHT1, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0]) """
    glEnable(GL_LIGHT1)
    glLightfv(GL_LIGHT1, GL_POSITION, [0.0, 3.0, -3.0, 1.0]) 
    glLightfv(GL_LIGHT1, GL_DIFFUSE, [1.0, 0.6, 0.1, 1.0])    
    glLightfv(GL_LIGHT1, GL_LINEAR_ATTENUATION, 0.05)         
 

    # Criar os objetos
    global my_garage, my_door
    my_garage = Garage()
    my_door = Door()

def draw_axes():
    glDisable(GL_LIGHTING)
    glBegin(GL_LINES)
    glColor3f(1,0,0); glVertex3f(0,0,0); glVertex3f(5,0,0)
    glColor3f(0,1,0); glVertex3f(0,0,0); glVertex3f(0,5,0)
    glColor3f(0,0,1); glVertex3f(0,0,0); glVertex3f(0,0,5)
    glEnd()
    glEnable(GL_LIGHTING)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    # Configurar Câmara
    rad_yaw = math.radians(cam_yaw)
    look_x = cam_x + math.sin(rad_yaw)
    look_y = cam_y 
    look_z = cam_z + math.cos(rad_yaw) 
    gluLookAt(cam_x, cam_y, cam_z, look_x, look_y, look_z, 0.0, 1.0, 0.0)
    
    # Desenhar Cena
    draw_axes()
    
    if my_garage: my_garage.draw()
    if my_door: 
        my_door.draw()
        if my_door.update(): 
            glutPostRedisplay() 

    glutSwapBuffers()

def keyboard(key, x, y):
    global cam_x, cam_z, cam_yaw
    
    # Interação com a Porta
    if key == b'g' and my_door: 
        my_door.trigger()
        glutPostRedisplay()

    # Movimento Câmara (WASD)
    rad_yaw = math.radians(cam_yaw)
    if key == b'w':
        cam_x += math.sin(rad_yaw) * CAM_SPEED
        cam_z += math.cos(rad_yaw) * CAM_SPEED
    elif key == b's':
        cam_x -= math.sin(rad_yaw) * CAM_SPEED
        cam_z -= math.cos(rad_yaw) * CAM_SPEED
    elif key == b'a': cam_yaw -= ROT_SPEED
    elif key == b'd': cam_yaw += ROT_SPEED

    glutPostRedisplay()

def reshape(w, h):
    if h == 0: h = 1
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, w / h, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

if __name__ == "__main__":
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"Projeto CG - Movimento da camara WASD")
    init()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutMainLoop()
