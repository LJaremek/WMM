import moderngl
from pyrr import Matrix44, Vector4

from base_window import BaseWindowConfig


class PhongWindow(BaseWindowConfig):
    def __init__(self, **kwargs):
        super(PhongWindow, self).__init__(**kwargs)
        self._colour = Vector4((0.75, 0.0, 1.0, 1.0))

    def init_shaders_variables(self):
        self._sphere = self.load_scene("sphere.obj")
        self._lookat = self.program["lookat"]

    def render(self, time: float, frame_time: float):
        self.ctx.clear(1.0, 1.0, 1.0, 0.0)
        self.ctx.enable(moderngl.DEPTH_TEST | moderngl.CULL_FACE)

        proj = Matrix44.perspective_projection(
            45.0,
            self.aspect_ratio,
            0.1,
            1000.0
            )

        lookat = Matrix44.look_at(
            (3.0, 1.0, -5.0),
            (0.0, 0.0, 1.0),
            (0.0, 0.0, 1.0),
        )

        self._lookat.write(lookat.astype("f4"))
        self.vao.render()
