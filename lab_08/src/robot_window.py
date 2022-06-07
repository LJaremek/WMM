from math import pi

from moderngl.vertex_array import VertexArray
from pyrr import Matrix44, Vector4
import moderngl

from base_window import BaseWindowConfig


class RobotWindow(BaseWindowConfig):
    def __init__(self, **kwargs) -> None:
        super(RobotWindow, self).__init__(**kwargs)
        self._vectors = {
            "head": (0,  0,    5),
            "body": (0,  0,    2),
            "arml": (0, -3,    3),
            "armr": (0,  3,    3),
            "legl": (0, -2, -1.5),
            "legr": (0,  2, -1.5)
        }

        self._scales = {
            "head": (1,     1,    1),
            "body": (1,     1,    2),
            "arml": (0.5, 0.5, 1.25),
            "armr": (0.5, 0.5, 1.25),
            "legl": (0.5, 0.5, 1.75),
            "legr": (0.5, 0.5, 1.75)
        }

        self._rotations = {
            "head": 0,
            "body": 0,
            "arml":  pi/4,
            "armr": -pi/4,
            "legl":  pi/6,
            "legr": -pi/6
        }

        self._colours = {  # R, G, B, A
            "head": Vector4((1, 1, 1, 1)),
            "body": Vector4((1, 0, 0, 1)),
            "arml": Vector4((1, 1, 0, 1)),
            "armr": Vector4((1, 1, 0, 1)),
            "legl": Vector4((0, 0, 0, 1)),
            "legr": Vector4((0, 0, 0, 1)),
        }

    def _render_element(self,
                        object: VertexArray,
                        projection: Matrix44,
                        lookat: Matrix44,
                        trasnlation: tuple,
                        scale: tuple,
                        rotation: float,
                        colour: Vector4
                        ) -> None:

        scale = Matrix44.from_scale(scale)
        rotation = Matrix44.from_x_rotation(rotation)
        trasnlation = Matrix44.from_translation(trasnlation)

        pvm = projection * lookat * trasnlation * rotation * scale

        self._pvm_matrix.write(pvm.astype("f4"))
        self._obj_colours.write(colour.astype("f4"))

        object.render()

    def model_load(self) -> None:
        self._sphere = self.load_scene("sphere.obj")
        self._vao_sphere = self._sphere.root_nodes[0]. \
            mesh.vao.instance(self.program)
        self._cube = self.load_scene("cube.obj")
        self._vao_cube = self._cube.root_nodes[0]. \
            mesh.vao.instance(self.program)

    def init_shaders_variables(self) -> None:
        self._pvm_matrix = self.program["pvm_matrix"]
        self._obj_colours = self.program["obj_color"]

    def render(self, time: float, frame_time: float) -> None:
        self.ctx.clear(0.8, 0.8, 0.8, 0.0)
        self.ctx.enable(moderngl.DEPTH_TEST)

        projection = Matrix44.perspective_projection(
            45.0,
            self.aspect_ratio,
            0.1,
            1000.0
            )

        lookat = Matrix44.look_at(
            (-25, -19, 6),
            (0,     0, 1),
            (0,     0, 1),
        )

        for part in ("head", "body", "arml", "armr", "legl", "legr"):
            if part == "head":
                vao = self._vao_sphere
            else:
                vao = self._vao_cube

            self._render_element(
                vao,
                projection,
                lookat,
                self._vectors[part],
                self._scales[part],
                self._rotations[part],
                self._colours[part]
                )
