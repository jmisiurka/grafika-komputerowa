import glm
from OpenGL.GL import *
from OpenGL.GLU import *

class PointLight:
    def __init__(self, shader_program, position, color):
        self.position = position
        self.positionLoc = glGetUniformLocation(shader_program, "pointLight.position")
        glUniform3fv(self.positionLoc, 1, glm.value_ptr(self.position))
        
        self.color = color
        self.colorLoc = glGetUniformLocation(shader_program, "pointLight.color")
        glUniform3fv(self.colorLoc, 1, glm.value_ptr(self.color))

    def update_position(self, position):
        glUniform3fv(self.positionLoc, 1, glm.value_ptr(position))
        self.position = position
        print(f"Light position: {position}")

    def update_color(self, color):
        red = self.color[0]
        green = self.color[1]
        blue = self.color[2]
        
        if color == 'r':
            red += 0.1
            if red > 1:
                red -= 1

        if color == 'g':
            green += 0.1
            if green > 1:
                green -= 1

        if color == 'b':
            blue += 0.1
            if blue > 1:
                blue -= 1
        
        color = glm.vec3(red, green, blue)

        glUniform3fv(self.colorLoc, 1, glm.value_ptr(color))
        self.color = color
        print(f"Light color: {self.color}")

def make_directional_light(shader_program, direction, color):
    lightColorLoc = glGetUniformLocation(shader_program, 'directionalLight.color')
    glUniform3fv(lightColorLoc, 1, glm.value_ptr(color))

    lightDirectionLoc = glGetUniformLocation(shader_program, 'directionalLight.direction')
    glUniform3fv(lightDirectionLoc, 1, glm.value_ptr(direction))