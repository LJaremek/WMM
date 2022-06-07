#version 330

// const vec3 light_position = vec3(1.0, 200, 1.0);
// const vec4 light_color = vec4(1.0, 1.0, 0.0, 1.0);
// const float ambient = 0.2;

uniform vec4 obj_color;

in vec3 v_postion;
in vec3 v_normal;
out vec4 f_color;

void main()
{
    f_color = obj_color;
}
