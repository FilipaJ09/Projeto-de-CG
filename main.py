import sys, os
import math
import time
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import Image

# --- Importar objetos ---
from objects.garage import Garage
from objects.garage_door import Door
from objects.extra_elem import Extra_elem
from objects.obj_loader import OBJModel
from objects.car import Car

# --- Variáveis globais ---
my_garage = None
my_door = None
car = None 
tex_floor = None

# Dicionários de controlo
keys = {}   # Guarda teclas premidas
assets = {} # Guarda modelos 3D extras

# Path da imagem de textura
FLOOR_PATH  = "floor2_mosaic.jpg" 

# Configuração da Câmara
cam_x, cam_y, cam_z = 0.0, 2.0, 15.0 # Começar um pouco mais perto e baixo
cam_yaw = 180.0   # Rotação horizontal (olhar para trás inicialmente)
cam_pitch = 0.0   # Rotação vertical (olhar em frente)
CAM_SPEED = 0.2   # Velocidade de movimento
ROT_SPEED = 2.0   # Velocidade de rotação

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

def init():
    # Configurações globais
    glClearColor(0.05, 0.05, 0.1, 1.0) # Cor de fundo (Noite)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
    glEnable(GL_NORMALIZE) 
    
    # LUZ 0: Ambiente/Lua
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, [10.0, 20.0, 20.0, 1.0])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.1, 0.1, 0.15, 1.0]) 
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.1, 0.1, 0.2, 1.0])

    # LUZ 1: Interior da Garagem (Quente)
    glEnable(GL_LIGHT1)
    glLightfv(GL_LIGHT1, GL_POSITION, [0.0, 3.0, -3.0, 1.0]) 
    glLightfv(GL_LIGHT1, GL_DIFFUSE, [1.0, 0.6, 0.1, 1.0])    
    glLightfv(GL_LIGHT1, GL_LINEAR_ATTENUATION, 0.05)         

    # Criar os objetos principais
    global my_garage, my_door, tex_floor, car
    my_garage = Garage()
    my_door = Door()
    car = Car() # Certifica-te que o car.py está atualizado (versão sem pywavefront ou com caminhos corrigidos)

    # Carregar Textura do Chão
    tex_floor = load_texture(FLOOR_PATH, repeat=True)

    # Carregar Assets Extras
    try:
        print("A carregar modelos extra...")
        # Nota: Certifica-te que estes ficheiros .obj existem na pasta ou ajusta os nomes
        assets["arvore"] = Extra_elem("Arvore.obj")
        assets["candeeiro"] = Extra_elem("CandeeiroRua.obj")
        assets["banco"] = Extra_elem("BancoJardim.obj")
        assets["seta"] = Extra_elem("SetaGaragem.obj")
        assets["trio"] = Extra_elem("GirlTrio.obj")
    except Exception as e:
        print(f"Aviso ao carregar extras: {e}")

def draw_floor():
    S = 100.0   
    T = 50.0 
    if tex_floor:
        glEnable(GL_TEXTURE_2D) 
        glBindTexture(GL_TEXTURE_2D, tex_floor)
    
    glColor3f(1, 1, 1)
    glNormal3f(0, 1, 0)

    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0); glVertex3f(-S, 0.0,  S)
    glTexCoord2f(T,   0.0); glVertex3f( S, 0.0,  S)
    glTexCoord2f(T,    T ); glVertex3f( S, 0.0, -S)
    glTexCoord2f(0.0,  T ); glVertex3f(-S, 0.0, -S)
    glEnd()
    
    glDisable(GL_TEXTURE_2D)  

def draw_scene_objects():
    """Desenha os elementos decorativos"""
    
    # Candeeiro
    if "candeeiro" in assets:
        assets["candeeiro"].draw(location=(-8, 0, 15), scale=(0.5,0.5,0.5))
        # Luz do Candeeiro (simulada)
        glEnable(GL_LIGHT2)
        glLightfv(GL_LIGHT2, GL_POSITION, [-8.0, 4.5, 15.0, 1.0])
        glLightfv(GL_LIGHT2, GL_DIFFUSE, [1.0, 1.0, 0.8, 1.0]) 
        glLightfv(GL_LIGHT2, GL_QUADRATIC_ATTENUATION, 0.02) 

    # Árvores
    if "arvore" in assets:
        assets["arvore"].draw(location=(12, 0, 5), scale=(1.2, 1.2, 1.2))
        assets["arvore"].draw(location=(-15, 0, 10), scale=(1.5, 1.5, 1.5), angle=90)

    # Outros
    if "banco" in assets:
        assets["banco"].draw(location=(-6, 0, 14), angle=180)
    
    if "trio" in assets:
        assets["trio"].draw(location=(5, 0, 10), angle=-30)
        
    if "seta" in assets:
        rot = (time.time() * 50) % 360
        assets["seta"].draw(location=(0, 5, 8), scale=(0.5,0.5,0.5), angle=rot, rotation=(0,1,0))

def update_camera_logic():
    global cam_x, cam_y, cam_z, cam_yaw, cam_pitch

    # 1. Atualizar Ângulos (Olhar) - CORRIGIDO (Sinais Trocados)
    if keys.get(GLUT_KEY_LEFT):  cam_yaw += ROT_SPEED  # Trocado de -= para +=
    if keys.get(GLUT_KEY_RIGHT): cam_yaw -= ROT_SPEED  # Trocado de += para -=
    
    if keys.get(GLUT_KEY_UP):    cam_pitch += ROT_SPEED 
    if keys.get(GLUT_KEY_DOWN):  cam_pitch -= ROT_SPEED 

    # Limitar o Pitch
    if cam_pitch > 89: cam_pitch = 89
    if cam_pitch < -89: cam_pitch = -89

    # 2. Calcular Vetores
    rad_yaw = math.radians(cam_yaw)
    
    # Frente 
    fw_x = math.sin(rad_yaw) * CAM_SPEED
    fw_z = math.cos(rad_yaw) * CAM_SPEED
    
    # Direita
    rt_x = math.cos(rad_yaw) * CAM_SPEED
    rt_z = -math.sin(rad_yaw) * CAM_SPEED

    # 3. Aplicar Movimento (WASD) - CORRIGIDO (A e D trocados)
    if keys.get(b'w'): # Frente
        cam_x += fw_x
        cam_z += fw_z
    if keys.get(b's'): # Trás
        cam_x -= fw_x
        cam_z -= fw_z
        
    # CORREÇÃO AQUI: Invertemos os sinais do A e D
    if keys.get(b'd'): # Direita (estava a ir para a esquerda)
        cam_x -= rt_x  # Mudado de += para -=
        cam_z -= rt_z
    if keys.get(b'a'): # Esquerda (estava a ir para a direita)
        cam_x += rt_x  # Mudado de -= para +=
        cam_z += rt_z
        
    # Levitar
    if keys.get(b' '): cam_y += 0.2
    if keys.get(b'x'): cam_y -= 0.2

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    # 1. Processar Inputs e Lógica
    update_camera_logic()
    if my_door: my_door.update()

    # 2. Configurar a Câmara (gluLookAt)
    # Converter graus para radianos
    rad_yaw = math.radians(cam_yaw)
    rad_pitch = math.radians(cam_pitch)

    # Calcular para onde estamos a olhar (Target)
    # A coordenada Y do alvo depende do pitch (olhar cima/baixo)
    # As coordenadas X e Z dependem do yaw E do pitch (encolhem se olharmos muito para cima)
    look_dir_y = math.sin(rad_pitch)
    horizontal_scale = math.cos(rad_pitch)
    look_dir_x = math.sin(rad_yaw) * horizontal_scale
    look_dir_z = math.cos(rad_yaw) * horizontal_scale

    # Definir câmara: Posição -> Posição + Direção -> Cima
    gluLookAt(cam_x, cam_y, cam_z,
              cam_x + look_dir_x, cam_y + look_dir_y, cam_z + look_dir_z,
              0.0, 1.0, 0.0)

    # 3. Desenhar Cena
    draw_floor()
    draw_scene_objects()
    
    if car: car.draw_car()
    if my_garage: my_garage.draw()
    if my_door: my_door.draw()
    
    glutSwapBuffers()
    glutPostRedisplay()

# --- Callbacks de Teclado ---
def keyboard_down(key, x, y):
    keys[key] = True
    if key in (b'\x1b', b'q'): sys.exit(0)
    if key == b'g' and my_door: my_door.trigger()

def keyboard_up(key, x, y):
    keys[key] = False

def special_down(key, x, y):
    keys[key] = True

def special_up(key, x, y):
    keys[key] = False

def reshape(w, h):
    if h == 0: h = 1
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, float(w) / float(h), 0.1, 200.0)
    glMatrixMode(GL_MODELVIEW)

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1024, 768) 
    glutCreateWindow(b"Garagem CG ")
    
    init()
    
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    
    # Registar callbacks
    glutKeyboardFunc(keyboard_down)
    glutKeyboardUpFunc(keyboard_up)
    glutSpecialFunc(special_down)
    glutSpecialUpFunc(special_up)
    
    print("\n=== Comandos ===")
    print("WASD: Mover (Frente/Tras/Lados)")
    print("Setas: Olhar (Cima/Baixo/Esq/Dir)")
    print("Espaço/X: Subir/Descer altura")
    print("G: Abrir Garagem")
    print("Q/ESC: Sair")
    
    glutMainLoop()
    
if __name__ == "__main__":
    main()