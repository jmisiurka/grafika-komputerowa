from OpenGL.GL import *
from OpenGL.GLU import *

def shaders():
    vertex_shader_source = open('shaders/v_shader.glsl').read()
    fragment_shader_source = open('shaders/f_shader.glsl').read()
    vertex_shader = glCreateShader(GL_VERTEX_SHADER)
    glShaderSource(vertex_shader, vertex_shader_source)
    glCompileShader(vertex_shader)
    if not glGetShaderiv(vertex_shader, GL_COMPILE_STATUS):
        print('Vertex shader compilation failed:')
        print(glGetShaderInfoLog(vertex_shader))

    fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(fragment_shader, fragment_shader_source)
    glCompileShader(fragment_shader)
    if not glGetShaderiv(fragment_shader, GL_COMPILE_STATUS):
        print('Fragment shader compilation failed:')
        print(glGetShaderInfoLog(fragment_shader))

    shader_program = glCreateProgram()
    glAttachShader(shader_program, vertex_shader)
    glAttachShader(shader_program, fragment_shader)
    glLinkProgram(shader_program)
    if not glGetProgramiv(shader_program, GL_LINK_STATUS):
        print('Shader program linking failed:')
        print(glGetProgramInfoLog(shader_program))

    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)

    return shader_program