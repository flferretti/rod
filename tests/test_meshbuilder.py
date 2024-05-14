import os
import pathlib
import tempfile

import numpy as np
import trimesh

from rod.builder.primitives import MeshBuilder


def test_builder_creation():
    mesh = trimesh.creation.box([1, 1, 1])
    print(mesh.vertices.shape)

    # Temporary write to file because rod Mesh works with uri
    with tempfile.NamedTemporaryFile() as fp:
        # fp.write(trimesh.exchange.stl.export_stl(mesh))
        mesh.export(fp.name, file_type="stl")

        builder = MeshBuilder(
            name="test_mesh",
            mesh_path=fp.name,
            mass=1.0,
            scale=np.array([1.0, 1.0, 1.0]),
        )
        assert (
            builder.mesh.vertices.shape == mesh.vertices.shape
        ), f"{builder.mesh.vertices.shape} != {mesh.vertices.shape}"
        assert (
            builder.mesh.faces.shape == mesh.faces.shape
        ), f"{builder.mesh.faces.shape} != {mesh.faces.shape}"
        assert (
            builder.mesh.moment_inertia.all() == mesh.moment_inertia.all()
        ), f"{builder.mesh.moment_inertia} != {mesh.moment_inertia}"
        assert (
            builder.mesh.volume == mesh.volume
        ), f"{builder.mesh.volume} != {mesh.volume}"


def test_builder_creation_custom_mesh():
    # Create a custom mesh
    vertices = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]])
    faces = np.array([[0, 1, 2], [0, 2, 3]])
    custom_mesh = trimesh.Trimesh(vertices=vertices, faces=faces)

    # Temporary write to file because rod Mesh works with uri
    filename = pathlib.Path(__file__).parent / "test_custom_mesh.stl"
    custom_mesh.export(filename)

    builder = MeshBuilder(
        name="test_custom_mesh",
        mesh_path=filename,
        mass=1.0,
        scale=np.array([1.0, 1.0, 1.0]),
    )

    # Assert on meshes (builder mesh vs custom_mesh)
    try:
        assert builder.mesh.vertices.shape == custom_mesh.vertices.shape
        assert builder.mesh.faces.shape == custom_mesh.faces.shape
        assert builder.mesh.moment_inertia.all() == custom_mesh.moment_inertia.all()
        assert builder.mesh.volume == custom_mesh.volume
    finally:
        os.remove(filename)
