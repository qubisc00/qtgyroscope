from pyrr import Matrix44

#----------------
#	Projection
#----------------

def orthographic(w, h):
	return Matrix44.orthogonal_projection(
			0, w, h, 0, 1, -1, dtype='f4')