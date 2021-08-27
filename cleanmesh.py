import numpy as np
import pymesh


def cleanup_mesh(mesh: pymesh.Mesh, verbose: bool = True):
	if verbose: print("Removing duplicated triangles...", end="")
	mesho1, duplicated_triangles = pymesh.remove_duplicated_faces(mesh)  # remove duplicate triangles
	s = duplicated_triangles["ori_face_index"]
	if verbose: print(f" removed {len(s)}")
	
	if verbose: print("Removing obtuse triangles...", end="")
	mesho2, obtuse_triangles = pymesh.remove_obtuse_triangles(mesho1, max_angle=120, max_iterations=5)  # remove bad triangles?
	s = obtuse_triangles["num_triangle_split"]
	if verbose: print(f" removed {s}")
	
	if verbose: print("Removing degenerative triangles...", end="")
	mesho3, ori_face_indices = pymesh.remove_degenerated_triangles(mesho2, num_iterations=5)  # rm triangles with area 0
	s = ori_face_indices["ori_face_indices"]
	if verbose: print(f" removed {len(s)}")
	
	if verbose: print("Removing unused vertices...", end="")
	mesho4, removed_lines = pymesh.remove_isolated_vertices(mesho3)  # rm unused vertices, lines that are not used in a triangle
	s = removed_lines["num_vertex_removed"]
	if verbose: print(f" removed {s} lines")
	
	if verbose: print("Removing duplicated vertices...", end="")
	mesho5, duplicated_lines = pymesh.remove_duplicated_vertices(mesho4)  # rm duplicate vertices/lines
	s = duplicated_lines.get("num_vertex_merged")
	if verbose: print(f" removed {s}")
	return mesho5

def remove_empty_volume_from_top(volume):
	for index, i in enumerate(range(len(volume) - 1)):
		# if verbose: print(f"I:{i} T:{len(triangles)}", end=", ")
		for j in range(len(volume[i]) - 1):
			if np.count_nonzero(volume[i][j]) != 0:
				remove_from_top = index
				stop = True
				break
	return volume[:remove_from_top, :, :]


def remove_empty_volume_from_bottom(volume):
	for index, i in enumerate(range(len(volume) - 1, 0, -1)):
		# if verbose: print(f"I:{i} T:{len(triangles)}", end=", ")
		for j in range(len(volume[i]) - 1, 0, -1):
			if np.count_nonzero(volume[i][j]) != 0:
				remove_from_bottom = index
				stop = True
				break
		if stop: break
	return volume[remove_from_bottom:, :, :]

def remove_empty_volume_around_mesh(volume):
	volume1 = remove_empty_volume_from_top(volume)
	volume2 = remove_empty_volume_from_bottom(volume1)
	return volume2
