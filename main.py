import sys, os
import math
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import Image

# --- Importar objetos ---
from objects.garage import Garage
from objects.garage_door import Door
from objects.extra_elem import Extra_elem
from objects import obj_loader
from objects.car import Car

# --- Variaveis globais ---
my_garage = None
my_door = None
extra_elems = None
tex_floor = None
car = None #carro

# Path da imagem de textura
FLOOR_PATH  = "floor2_mosaic.jpg" 
# Paths dos elementos extra que podem ser desenhados
SETA_PATH = "SetaGaragem.obj"
BANCO_PATH = "BancoJardim.obj"
TRIO_PATH = "GirlTrio.obj"
CANDEEIRO_PATH = "CandeeiroRua.obj"
ARVORE_PATH = "Arvore.obj"

# Câmara
cam_x, cam_y, cam_z = 0.0, 6.0, 20.0
cam_yaw = 180.0 
CAM_SPEED = 0.5
ROT_SPEED = 3.0

# Lista de comandos
comandos = [
    "W - mover a câmara para frente",
    "S - mover a câmara para trás",
    "A - mover a câmara para a esquerda",
    "D - mover a câmara para a direita",
    "G - abrir porta da garagem",
    "ESC/Q - sair do programa",
    "H - ver lista de comandos"
]

def load_texture(path, repeat=True): 
    # NOTA: o código desta função consiste no código disponibilizado pelos professores nos ficheiros das TPs de CG
    """Recebe o path de uma imagem e carrega essa textura no programa, 
        devolvendo o id da textura para que depois possa ser aplicada
        no desenho dos objetos."""
    # Verificar se o caminho do ficheiro existe
    if not os.path.isfile(path):
        print("Texture not found:", path)
        sys.exit(1)
    base_dir = os.path.dirname(__file__)   # pasta onde está extra_elem.py
    path = os.path.join(base_dir, path)
    
    # Abrir imagem e converter para RGBA
    img = Image.open(path).convert("RGBA")
    w, h = img.size # Obter dimensões da imagem
    # Converter a imagem para bytes -> para o OpenGL poder usar/entender
    data = img.tobytes("raw", "RGBA", 0, -1)

    # Criar e ligar textura
    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)

    # Filtros
    # Definem como a textura é reduzida e ampliada (neste caso (mipmaps +) interpolação linear), evitando que a textura fique pixelizada, por exemplo 
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR) 
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    # Mipmaps 
    # Define o que acontece quando a textura ultrapassa os limites do objeto onde está a ser usada
    # Caso repeat = True, a textura é repetida infinitamente.
    # Caso contrário, estica-se apenas a última linha/coluna até à borda
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT if repeat else GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT if repeat else GL_CLAMP_TO_EDGE)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

    # Criação de mipmaps com o GLU
    gluBuild2DMipmaps(GL_TEXTURE_2D, GL_RGBA, w, h, GL_RGBA, GL_UNSIGNED_BYTE, data)

    # Devolve o ID de cada textura carregada que será usado quando os objectos forem desenhados
    return tex_id

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
    global my_garage, my_door, extra_elems, tex_floor, car
    my_garage = Garage()
    my_door = Door()
    car = Car()

    # Carregar as texturas
    tex_floor = load_texture(FLOOR_PATH,repeat=True)

def draw_axes():
    glDisable(GL_LIGHTING)
    glBegin(GL_LINES)
    glColor3f(1,0,0); glVertex3f(0,0,0); glVertex3f(5,0,0)
    glColor3f(0,1,0); glVertex3f(0,0,0); glVertex3f(0,5,0)
    glColor3f(0,0,1); glVertex3f(0,0,0); glVertex3f(0,0,5)
    glEnd()
    glEnable(GL_LIGHTING)

def draw_floor():
    S = 100.0   # Chão será 200x200    
    T = 50.0 # Fator de repetição da textura no chão, pois para valores superiores a 1.0, o OpenGL coloca em ação o modo de wrap e faz repetição de mosaicos
    glEnable(GL_TEXTURE_2D) 
    glBindTexture(GL_TEXTURE_2D, tex_floor)
    glColor3f(1, 1, 1)        # Não mexer na cor
    glNormal3f(0, 1, 0)

    # Definição dos vértices do chão e aplicação da textura
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0); glVertex3f(-S, 0.0,  S)
    glTexCoord2f(T,   0.0); glVertex3f( S, 0.0,  S)
    glTexCoord2f(T,    T ); glVertex3f( S, 0.0, -S)
    glTexCoord2f(0.0,  T ); glVertex3f(-S, 0.0, -S)
    glEnd()
    glDisable(GL_TEXTURE_2D)  
    
def draw_extra_elems():
    girl_trio = Extra_elem(SETA_PATH)
    girl_trio.draw(location=(5,5,5))

    
    # TODO
    # Corrigir esta função
    # Desenhar todos os objetos
    
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
    draw_floor()
    draw_axes()
    draw_extra_elems()
    car.draw_car()
    
    if my_garage: my_garage.draw()
    if my_door: 
        my_door.draw()
        if my_door.update(): 
            glutPostRedisplay() 
    
    glutSwapBuffers()

def keyboard(key, x, y):
    global cam_x, cam_z, cam_yaw
    
    # Sair do programa
    if key in (b'\x1b', b'q'):
        try:
            glutLeaveMainLoop()
        except Exception:
            sys.exit(0)
            
    # Interação com a Porta
    if key == b'g' and my_door: 
        my_door.trigger()
        glutPostRedisplay()
    
    # Mostrar comandos
    if key == b'h': mostrar_comandos()

    # --- CÁLCULO DO MOVIMENTO ---
    rad_yaw = math.radians(cam_yaw)
    
    # Vetor "Frente" (para onde estamos a olhar)
    front_x = math.sin(rad_yaw) * CAM_SPEED
    front_z = math.cos(rad_yaw) * CAM_SPEED
    
    # Vetor "Direita" (90 graus em relação à frente)
    # Matematicamente, para rodar 90 graus: (x, z) -> (z, -x)
    right_x = math.cos(rad_yaw) * CAM_SPEED
    right_z = -math.sin(rad_yaw) * CAM_SPEED

    # Movimento Frente/Trás (W/S)
    if key == b'w':
        cam_x += front_x
        cam_z += front_z
    elif key == b's':
        cam_x -= front_x
        cam_z -= front_z
        
    # Movimento Lateral (A/D) - "Strafe"
    elif key == b'a': # Esquerda (Inverso da direita)
        cam_x -= right_x
        cam_z -= right_z
    elif key == b'd': # Direita
        cam_x += right_x
        cam_z += right_z

    # Movimento Carro (TODO)

    # Interação com as Portas do Carro (TODO)

    glutPostRedisplay()


def special_keys(key, x, y):
    global cam_yaw
    
    # Rodar a câmara com as setas
    if key == GLUT_KEY_LEFT:
        cam_yaw -= ROT_SPEED
    elif key == GLUT_KEY_RIGHT:
        cam_yaw += ROT_SPEED

    # Atualizar o ecrã
    glutPostRedisplay()

def reshape(w, h):
    if h == 0: h = 1
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, float(w) / float(h), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def mostrar_comandos():
    """Imprime os comandos que o utilizador pode utilizar para interagir
        com o programa"""
    print("\n=== Comandos disponíveis ===")
    for cmd in comandos:
        print(cmd)
    print("============================\n")

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600) 
    glutCreateWindow(b"Projeto CG - Movimento da camara WASD")
    init()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(special_keys)
    glutMainLoop()
    
if __name__ == "__main__":
    mostrar_comandos()
    main()
