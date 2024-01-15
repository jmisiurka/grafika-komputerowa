import math
from os import read
import random
import glfw
from glfw import *

import numpy as np
import glm

from PIL import Image

from OpenGL.GL import *
from OpenGL.GLU import *

from shaders import shaders
from textures import load_texture
from camera import *
from models import sierpinski_make
from models import vertices
from models import floor_vertices
from light import *


WIDTH = 1920
HEIGHT = 1080

# global variables
camera = Camera(0)
shader_program = 0
textures_on = False
light = None

def main ():
    global camera, shader_program, light

    size = 5
    levels = int(sys.argv[1])

    # initialization of glfw and openGL
    if not glfw.init():
        print("Failed to init glfw")
        return

    window = glfw.create_window(WIDTH, HEIGHT, "Sierpinski", None, None)

    if not window:
        print("Failed to open window")
        return

    glfw.make_context_current(window)
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
    
    glfw.set_key_callback(window, key_callback)
    glfw.set_cursor_pos_callback(window, mouse_callback)
    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)


    glEnable(GL_DEPTH_TEST)

    shader_program = shaders()
    glUseProgram(shader_program)

    # piramids
    vbo, vao = glGenBuffers(1), glGenVertexArrays(1)
    
    glBindVertexArray(vao)

    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW)

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))
    glEnableVertexAttribArray(1)

    glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(24))
    glEnableVertexAttribArray(2)

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)


    # floor
    vbo_floor, vao_floor = glGenBuffers(1), glGenVertexArrays(1)

    glBindVertexArray(vao_floor)
    
    glBindBuffer(GL_ARRAY_BUFFER, vbo_floor)
    glBufferData(GL_ARRAY_BUFFER, floor_vertices, GL_STATIC_DRAW)

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))
    glEnableVertexAttribArray(1)

    glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(24))
    glEnableVertexAttribArray(2)

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)



    bricks = load_texture('textures/bricks.jpg')
    cobble = load_texture('textures/cobble.jpeg')

    objectColor = glm.vec3(1.0, 1.0, 1.0)
    objectColorLoc = glGetUniformLocation(shader_program, 'objectColor')
    glUniform3fv(objectColorLoc, 1, glm.value_ptr(objectColor))

    light = PointLight(shader_program, glm.vec3(5.0, 0.0, 3.0), glm.vec3(1.0, 0.0, 0.0))

    # light
    lightColor = glm.vec3(0.0, 0.0, 0.5)
    lightDirection = glm.vec3(1.0, -0.6, 0.0)
    
    make_directional_light(shader_program, lightDirection, lightColor)

    model = glm.mat4(1.0)
    modelLoc = glGetUniformLocation(shader_program, 'model')

    camera = Camera(shader_program)

    projection = glm.perspective(glm.radians(45.0), WIDTH / HEIGHT, 0.1, 1000.0)
    projectionLoc = glGetUniformLocation(shader_program, "projection")

    glUniformMatrix4fv(modelLoc, 1, GL_FALSE, glm.value_ptr(model))
    glUniformMatrix4fv(projectionLoc, 1, GL_FALSE, glm.value_ptr(projection))
    
    pyramids = sierpinski_make(size, levels)

    prev_time = glfw.get_time()

    rotation = 0



    # main loop
    while not glfw.window_should_close(window):
        process_input(window)

        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        camera.update()

        current_time = glfw.get_time()
        delta_time = current_time - prev_time
        prev_time = current_time

        rotation += 25 * delta_time

        if rotation > 360:
            rotation -= 360

        glBindTexture(GL_TEXTURE_2D, cobble)
        glBindVertexArray(vao_floor)
        model = glm.mat4(1.0)
        glUniformMatrix4fv(modelLoc, 1, GL_FALSE, glm.value_ptr(model))

        glDrawArrays(GL_TRIANGLES, 0, 6)

        glBindVertexArray(vao)

        for pyramid in pyramids:

            model = glm.mat4(1.0)
            model = glm.rotate(model, glm.radians(rotation), glm.vec3(0.0, 1.0, 0.0))
            model = glm.translate(model, pyramid)
            model = glm.scale(model, size * glm.vec3(1/(2**(levels - 1))))

            glUniformMatrix4fv(modelLoc, 1, GL_FALSE, glm.value_ptr(model))

            glBindTexture(GL_TEXTURE_2D, bricks)
            glDrawArrays(GL_TRIANGLES, 0, 21)


        glfw.swap_buffers(window)
        glfw.poll_events()


    glDeleteVertexArrays(1, vao)
    glDeleteBuffers(1, vbo)
    glDeleteProgram(shader_program)

    glfw.terminate()
    return


def process_input(window):
    # camera movement
    if (glfw.get_key(window, glfw.KEY_W) == glfw.PRESS):
        camera.camera_pos += 0.05 * camera.camera_front
    if (glfw.get_key(window, glfw.KEY_S) == glfw.PRESS):
        camera.camera_pos -= 0.05 * camera.camera_front
    if (glfw.get_key(window, glfw.KEY_D) == glfw.PRESS):
        camera.camera_pos += 0.05 * glm.normalize(glm.cross(camera.camera_front, camera.camera_up))
    if (glfw.get_key(window, glfw.KEY_A) == glfw.PRESS):
        camera.camera_pos -= 0.05 * glm.normalize(glm.cross(camera.camera_front, camera.camera_up))
    if (glfw.get_key(window, glfw.KEY_SPACE) == glfw.PRESS):
        camera.camera_pos += glm.vec3(0.0, 0.05, 0.0)
    if (glfw.get_key(window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS):
        camera.camera_pos -= glm.vec3(0.0, 0.05, 0.0)

    if camera.camera_pos.y < 0.1:
        camera.camera_pos.y = 0.1

def key_callback(window, key, scancode, action, mods):
    global textures_on, light, camera

    # switch textures
    if key == glfw.KEY_T and action == glfw.PRESS:
        if not textures_on:
            glUniform1i(glGetUniformLocation(shader_program, "texturesOn"), GL_TRUE)
            textures_on = True
        else:
            glUniform1i(glGetUniformLocation(shader_program, "texturesOn"), GL_FALSE)
            textures_on = False

    if key == glfw.KEY_KP_ADD and action == glfw.PRESS:
        camera.zoom *= 1.5
    if key == glfw.KEY_KP_SUBTRACT and action == glfw.PRESS:
        camera.zoom /= 1.5

    if key == glfw.KEY_UP and action == glfw.PRESS:
        light.update_position(light.position + glm.vec3(1.0, 0.0, 0.0))
    if key == glfw.KEY_DOWN and action == glfw.PRESS:
        light.update_position(light.position - glm.vec3(1.0, 0.0, 0.0))
    if key == glfw.KEY_RIGHT and action == glfw.PRESS:
        light.update_position(light.position + glm.vec3(0.0, 0.0, 1.0))
    if key == glfw.KEY_LEFT and action == glfw.PRESS:
        light.update_position(light.position - glm.vec3(0.0, 0.0, 1.0))
    if key == glfw.KEY_7 and action == glfw.PRESS:
        light.update_position(light.position + glm.vec3(0.0, 1.0, 0.0))
    if key == glfw.KEY_4 and action == glfw.PRESS:
        light.update_position(light.position - glm.vec3(0.0, 1.0, 0.0))

    if key == glfw.KEY_R and action == glfw.PRESS:
        light.update_color('r')
    if key == glfw.KEY_G and action == glfw.PRESS:
        light.update_color('g')
    if key == glfw.KEY_B and action == glfw.PRESS:
        light.update_color('b')

    # exit
    if (glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS):
        glfw.set_window_should_close(window, True)



def mouse_callback(window, x_pos, y_pos):
    camera.update_mouse(x_pos, y_pos)
   
# resize callback
def framebuffer_size_callback(window, width, height):
    glViewport(0, 0, width, height)

if __name__ == "__main__":

    main()