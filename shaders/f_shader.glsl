#version 330 core

out vec4 FragColor;

in vec2 texCoord;
in vec3 normal;
in vec3 fragPos;

uniform vec3 objectColor;
uniform vec3 viewPosition;
uniform sampler2D brickTexture;
uniform bool texturesOn;

struct DirectionalLight {
    vec3 direction;
    vec3 color;
};

struct PointLight {
    vec3 position;
    vec3 color;
};

uniform PointLight pointLight;
uniform DirectionalLight directionalLight;

vec3 applyDirectionalLight(DirectionalLight light, vec3 normal, vec3 viewDir, vec3 baseObject);
vec3 applyPointLight(PointLight light, vec3 normal, vec3 fragPos, vec3 viewDir, vec3 baseObject);

void main() 
{
    vec3 baseObject;

    if (texturesOn) {
        baseObject = vec3(texture(brickTexture, texCoord));
    } else {
        baseObject = objectColor;
    }

    vec3 viewDir = normalize(viewPosition - fragPos);

    // ambient lighting
    float ambientStrength = 0.1f;
    vec3 ambient = ambientStrength * vec3(1.0f);
    
    vec3 directional = applyDirectionalLight(directionalLight, normal, viewDir, baseObject);
    vec3 point = applyPointLight(pointLight, normal, fragPos, viewDir, baseObject);
    
    FragColor = vec4((directional + point), 1.0);
}

vec3 applyPointLight(PointLight light, vec3 normal, vec3 fragPos, vec3 viewDir, vec3 baseObject)
{
    vec3 lightDir = normalize(light.position - fragPos);

    vec3 diffuse = max(dot(normal, lightDir), 0.0f) * baseObject * light.color;

    //vec3 reflectDir = reflect(lightDir, normal);
    //vec3 specular = pow(max(dot(viewDir, reflectDir), 0.0f), 2) * 0.05f * baseObject * light.color;

    return diffuse; //(diffuse + specular);
}

vec3 applyDirectionalLight(DirectionalLight light, vec3 normal, vec3 viewDir, vec3 baseObject)
{
    vec3 normalizedLightDirection = normalize(-light.direction);

    // diffuse lighting
    float diffuse = max(dot(normalizedLightDirection, normal), 0.0f) * 0.5f;

    return diffuse * baseObject * light.color;
}