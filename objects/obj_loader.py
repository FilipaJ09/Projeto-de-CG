# NOTA: as seguintes classes foram criadas pelo professor André Falcão e disponibilizadas num ficheiro da TP11 de Computação Gráfica, estão aqui a ser usadas por ser até agora a única forma que conseguimos representar os objetos

import math
import ctypes
import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys, os
from PIL import Image

# -----------------------------------------------------------
# Classe Material para guardar cor difusa e textura
# -----------------------------------------------------------
class Material:
    def __init__(self, name):
        self.name = name
        self.diffuse = (1.0, 1.0, 1.0)   # cor difusa Kd
        self.texture_path = None         # caminho para a textura (se existir)
        self.texture_id = None           # id da textura OpenGL




# -----------------------------------------------------------
# Carregador de OBJ com VBOs e suporte a MTL + texturas
# -----------------------------------------------------------
class OBJModel:
    def __init__(self, filename):
        # Listas básicas de vértices, normais e coordenadas de textura
        self.vertices = []   # lista de (x, y, z)
        self.normals = []    # lista de (nx, ny, nz)
        self.texcoords = []  # lista de (u, v)

        # Cada face: { 'material': nome, 'verts': [(iv, it, in), ...] }
        self.faces = []

        # Materiais carregados do MTL
        self.materials = {}  # nome -> Material

        # Informação geométrica
        self.center = (0.0, 0.0, 0.0)  # centro do modelo no sistema de coordenadas original
        self.radius = 1.0              # raio aproximado (metade do maior lado do bounding box)

        # Batches de VBOs por material
        # cada elemento: {'material': nome, 'vbo': id, 'vertex_count': N}
        self.batches = []

        # Carrega o ficheiro OBJ (e MTL associado, se existir)
        self._load_obj(filename)
        self._compute_center_and_radius()
        self._build_gl_buffers()

    # -------------------------------------------------------
    # Carregamento do ficheiro OBJ 
    # -------------------------------------------------------
    def _load_obj(self, filename):
        base_dir = os.path.dirname(filename)
        if base_dir == "":
            base_dir = "."

        current_material = None

        # Função auxiliar para converter índice OBJ -> índice 0-based em Python
        # Aceita:
        #   >0  -> 1-based (1..N) → 0..N-1
        #   <0  -> relativo ao fim (-1 = último, -2 = penúltimo, etc)
        #    0  -> inválido → devolve -1 (marca "não existe")
        def resolve_index(idx_str, current_len):
            if not idx_str:
                return -1
            idx = int(idx_str)
            if idx > 0:
                return idx - 1
            elif idx < 0:
                return current_len + idx   # -1 → len-1, -2 → len-2, ...
            else:
                return -1

        try:
            with open(filename, "r", errors="ignore") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue

                    # Vértices de posição
                    if line.startswith("v "):
                        parts = line.split()
                        x, y, z = map(float, parts[1:4])
                        self.vertices.append((x, y, z))

                    # Coordenadas de textura
                    elif line.startswith("vt "):
                        parts = line.split()
                        u, v = map(float, parts[1:3])
                        self.texcoords.append((u, v))

                    # Normais
                    elif line.startswith("vn "):
                        parts = line.split()
                        nx, ny, nz = map(float, parts[1:4])
                        self.normals.append((nx, ny, nz))

                    # Referência ao ficheiro MTL
                    elif line.startswith("mtllib"):
                        _, mtl_name = line.split(None, 1)
                        mtl_name = mtl_name.strip()
                        mtl_path = os.path.join(base_dir, mtl_name)
                        self._load_mtl(mtl_path)

                    # Seleção de material
                    elif line.startswith("usemtl"):
                        _, mat_name = line.split(None, 1)
                        current_material = mat_name.strip()

                    # Faces (com suporte para índices negativos)
                    elif line.startswith("f "):
                        parts = line.split()[1:]
                        face_verts = []
                        for p in parts:
                            # Formatos possíveis:
                            #   v
                            #   v/vt
                            #   v//vn
                            #   v/vt/vn
                            tokens = p.split("/")

                            v_idx = resolve_index(tokens[0], len(self.vertices)) \
                                    if len(tokens) > 0 and tokens[0] else -1

                            vt_idx = resolve_index(tokens[1], len(self.texcoords)) \
                                     if len(tokens) > 1 and tokens[1] else -1

                            vn_idx = resolve_index(tokens[2], len(self.normals)) \
                                     if len(tokens) > 2 and tokens[2] else -1

                            face_verts.append((v_idx, vt_idx, vn_idx))

                        if len(face_verts) >= 3:
                            self.faces.append({
                                "material": current_material,
                                "verts": face_verts
                            })
        except OSError as e:
            print(f"Erro ao carregar OBJ '{filename}': {e}")
            sys.exit(1)

        if not self.vertices:
            print("OBJ não tem vértices. A sair.")
            sys.exit(1)

    # -------------------------------------------------------
    # Carregamento do ficheiro MTL, com suporte a map_Kd
    # -------------------------------------------------------
    def _load_mtl(self, mtl_path):
        base_dir = os.path.dirname(mtl_path)
        if base_dir == "":
            base_dir = "."

        current = None

        try:
            with open(mtl_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue

                    # Novo material
                    if line.startswith("newmtl"):
                        _, name = line.split(None, 1)
                        name = name.strip()
                        current = Material(name)
                        self.materials[name] = current

                    # Cor difusa Kd
                    elif line.startswith("Kd ") and current is not None:
                        parts = line.split()
                        r, g, b = map(float, parts[1:4])
                        current.diffuse = (r, g, b)

                    # Textura difusa map_Kd
                    elif line.startswith("map_Kd") and current is not None:
                        _, tex_name = line.split(None, 1)
                        tex_name = tex_name.strip()
                        tex_path = os.path.join(base_dir, tex_name)
                        current.texture_path = tex_path
        except OSError as e:
            print(f"Erro ao carregar MTL '{mtl_path}': {e}")
            # Não é fatal: podemos continuar sem materiais

        # Criar texturas OpenGL para todos os materiais que tenham map_Kd
        for mat in self.materials.values():
            if mat.texture_path is not None:
                mat.texture_id = self._create_texture(mat.texture_path)

    # -------------------------------------------------------
    # Criação de textura OpenGL a partir de ficheiro de imagem
    # -------------------------------------------------------
    def _create_texture(self, image_path):
        if not os.path.isfile(image_path):
            print(f"Aviso: textura '{image_path}' não encontrada.")
            return None

        try:
            img = Image.open(image_path)
            # OpenGL assume origem da imagem no canto inferior esquerdo
            img = img.transpose(Image.FLIP_TOP_BOTTOM)
            img = img.convert("RGBA")
            img_data = img.tobytes()
            width, height = img.size
        except Exception as e:
            print(f"Erro ao carregar textura '{image_path}': {e}")
            return None

        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)

        # Parâmetros da textura
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_RGBA,
            width,
            height,
            0,
            GL_RGBA,
            GL_UNSIGNED_BYTE,
            img_data
        )

        glBindTexture(GL_TEXTURE_2D, 0)
        return tex_id

    # -------------------------------------------------------
    # Cálculo do centro e raio do modelo (sem alterar a escala)
    # -------------------------------------------------------
    def _compute_center_and_radius(self):
        xs = [v[0] for v in self.vertices]
        ys = [v[1] for v in self.vertices]
        zs = [v[2] for v in self.vertices]

        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        min_z, max_z = min(zs), max(zs)

        cx = 0.5 * (min_x + max_x)
        cy = 0.5 * (min_y + max_y)
        cz = 0.5 * (min_z + max_z)
        self.center = (cx, cy, cz)

        size_x = max_x - min_x
        size_y = max_y - min_y
        size_z = max_z - min_z
        max_size = max(size_x, size_y, size_z)
        self.radius = max_size * 0.5 if max_size > 0 else 1.0

        # print(f"Centro do modelo: {self.center}, raio aproximado: {self.radius}") # filipa

    # -------------------------------------------------------
    # Construção dos VBOs (um por material) para desenhar com glDrawArrays
    # -------------------------------------------------------
    def _build_gl_buffers(self):
        # Dicionário temporário: nome_material -> lista de floats (vbo_data)
        temp_batches = {}

        for face in self.faces:
            mat_name = face["material"]
            verts = face["verts"]

            if mat_name not in temp_batches:
                temp_batches[mat_name] = []

            # Se não houver normais definidos, calculamos normal plana da face
            if all(v[2] < 0 for v in verts):
                v0 = self.vertices[verts[0][0]]
                v1 = self.vertices[verts[1][0]]
                v2 = self.vertices[verts[2][0]]

                ux, uy, uz = (v1[0] - v0[0], v1[1] - v0[1], v1[2] - v0[2])
                vx, vy, vz = (v2[0] - v0[0], v2[1] - v0[1], v2[2] - v0[2])
                nx = uy * vz - uz * vy
                ny = uz * vx - ux * vz
                nz = ux * vy - uy * vx
                length = math.sqrt(nx * nx + ny * ny + nz * nz)
                if length > 1e-8:
                    nx /= length
                    ny /= length
                    nz /= length
                else:
                    nx, ny, nz = 0.0, 0.0, 1.0
                face_normal = (nx, ny, nz)
            else:
                face_normal = None

            # Triangulação em "fan": (v0, vi, vi+1)
            for i in range(1, len(verts) - 1):
                tri = [verts[0], verts[i], verts[i + 1]]

                for (iv, it, in_idx) in tri:
                    px, py, pz = self.vertices[iv]

                    # Normal do vértice
                    if in_idx >= 0 and in_idx < len(self.normals):
                        nx, ny, nz = self.normals[in_idx]
                    else:
                        if face_normal is not None:
                            nx, ny, nz = face_normal
                        else:
                            nx, ny, nz = 0.0, 0.0, 1.0

                    # Coordenada de textura
                    if it >= 0 and it < len(self.texcoords):
                        u, v = self.texcoords[it]
                    else:
                        u, v = 0.0, 0.0

                    # Guardar em formato intercalado: pos (3), normal (3), tex (2)
                    temp_batches[mat_name].extend([px, py, pz, nx, ny, nz, u, v])

        # Criar VBO para cada batch
        for mat_name, data in temp_batches.items():
            if not data:
                continue

            arr = np.array(data, dtype=np.float32)
            vbo_id = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, vbo_id)
            glBufferData(GL_ARRAY_BUFFER, arr.nbytes, arr, GL_STATIC_DRAW)
            glBindBuffer(GL_ARRAY_BUFFER, 0)

            vertex_count = len(data) // 8  # 8 floats por vértice

            self.batches.append({
                "material": mat_name,
                "vbo": vbo_id,
                "vertex_count": vertex_count
            })

    # -------------------------------------------------------
    # Desenho do modelo usando VBOs (mantém escala original)
    # -------------------------------------------------------
    def draw(self):
        glPushMatrix()

        # Apenas centramos o modelo na origem (sem escala)
        glTranslatef(-self.center[0], -self.center[1], -self.center[2])

        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)

        stride = 8 * 4  # 8 floats * 4 bytes

        for batch in self.batches:
            mat_name = batch["material"]
            mat = self.materials.get(mat_name, None)

            # Selecionar material / textura
            if mat is not None and mat.texture_id is not None:
                glEnable(GL_TEXTURE_2D)
                glBindTexture(GL_TEXTURE_2D, mat.texture_id)
                glColor3f(1.0, 1.0, 1.0)  # deixa a textura controlar a cor
            else:
                glDisable(GL_TEXTURE_2D)
                if mat is not None:
                    glColor3f(*mat.diffuse)
                else:
                    glColor3f(0.8, 0.8, 0.8)

            glBindBuffer(GL_ARRAY_BUFFER, batch["vbo"])

            # Posição (3 floats a partir de offset 0)
            glVertexPointer(3, GL_FLOAT, stride, ctypes.c_void_p(0))
            # Normal (3 floats a partir de offset 12 bytes)
            glNormalPointer(GL_FLOAT, stride, ctypes.c_void_p(3 * 4))
            # Texcoords (2 floats a partir de offset 24 bytes)
            glTexCoordPointer(2, GL_FLOAT, stride, ctypes.c_void_p(6 * 4))

            glDrawArrays(GL_TRIANGLES, 0, batch["vertex_count"])

        glBindBuffer(GL_ARRAY_BUFFER, 0)

        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)
        glDisableClientState(GL_TEXTURE_COORD_ARRAY)

        glPopMatrix()
