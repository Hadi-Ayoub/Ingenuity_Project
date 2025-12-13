extends Node2D

@export var goal_position: Vector2i = Vector2i(2, 2) # grid coordinates

func get_tilemap() -> TileMapLayer:
	return find_child("MapCreator")

func get_goal_world_position(grid_size: float) -> Vector3:
	# Convert 2D grid coordinates → 3D world coordinates
	return Vector3(
		goal_position.x * grid_size,
		0,
		goal_position.y * grid_size
	)
