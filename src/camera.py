import glm
import math

from OpenGL.GL import *
from OpenGL.GLU import *

class Camera:
    def __init__(self, shader_program) -> None:
        self.pitch = 0.0
        self.yaw = -90.0

        self.zoom = 1

        self.last_x = 400
        self.last_y = 300

        self.camera_pos = glm.vec3(0.0, 1.0, 5.0)
        self.camera_front = glm.vec3(0.0, 0.0, -1.0)
        self.camera_up = glm.vec3(0.0, 1.0, 0.0)

        direction = glm.vec3(0)
        direction.x = math.cos(glm.radians(self.yaw))

        self.viewPositionLoc = glGetUniformLocation(shader_program, "viewPosition")
        self.viewLoc = glGetUniformLocation(shader_program, "view")

    def update(self):
        direction = glm.vec3(0)

        direction.x = math.cos(glm.radians(self.yaw)) * math.cos(glm.radians(self.pitch))
        direction.y = math.sin(glm.radians(self.pitch))
        direction.z = math.sin(glm.radians(self.yaw)) * math.cos(glm.radians(self.pitch))

        self.camera_front = glm.normalize(direction)

        view = glm.lookAt(self.camera_pos, self.camera_pos + self.camera_front, self.camera_up)
        view = glm.scale(view, glm.vec3(self.zoom, self.zoom, self.zoom))

        glUniformMatrix4fv(self.viewLoc, 1, GL_FALSE, glm.value_ptr(view))
        glUniform3fv(self.viewPositionLoc, 1, glm.value_ptr(self.camera_pos))

    def update_mouse(self, x_pos, y_pos):
        x_offset = x_pos - self.last_x
        y_offset = self.last_y - y_pos

        self.last_x = x_pos
        self.last_y = y_pos

        self.yaw += x_offset * 0.03
        self.pitch += y_offset * 0.03

        if self.pitch > 89:
            self.pitch = 89
        if self.pitch < -89:
            self.pitch = -89