extends Node3D

const Cell = preload("res://Cell/Cell.tscn")
const GoalScene = preload("res://Map/Goal.tscn")

@export var Map: PackedScene
@onready var worldEnvironment := $WorldEnvironment

var cells: Array = []
var goal: Node3D
var goal_reached := false

@onready var player: Node3D = $Player

func _process(_delta):
	if not goal_reached:
		check_goal_reached()


func check_goal_reached():
	if goal_reached or not goal:
		return

	print(player.global_position.distance_to(goal.global_position))
	if player.global_position.distance_to(goal.global_position) < 1.5:
		goal_reached = true
		print("GOAL REACHED!")
		

func get_farthest_tile(tiles: Array[Vector2i]) -> Vector2i:
	var start := Vector2i.ZERO
	var farthest := start
	var max_dist := -1.0

	for tile in tiles:
		var dist := tile.distance_to(start)
		if dist > max_dist:
			max_dist = dist
			farthest = tile

	return farthest




func _ready():
	var environment = get_tree().root.world_3d.fallback_environment
	environment.background_mode = Environment.BG_COLOR
	environment.background_color = Color.BLACK
	environment.ambient_light_color = Color("432d6d")

	generate_map()

func generate_map():
	if not Map is PackedScene:
		return

	# Instantiate 2D map OFF-SCENE (important!)
	var map: Node2D = Map.instantiate()

	var tile_map: TileMapLayer = map.get_tilemap()
	var used_tiles: Array[Vector2i] = tile_map.get_used_cells()

	# Spawn 3D cells
	for tile in used_tiles:
		var cell := Cell.instantiate()
		add_child(cell)
		cell.position = Vector3(
			tile.x * Globals.GRID_SIZE,
			0,
			tile.y * Globals.GRID_SIZE
		)
		cells.append(cell)

	for cell in cells:
		cell.update_faces(used_tiles)

	# Find goal tile at end of map
	var end_tile := get_farthest_tile(used_tiles)

	# Spawn goal
	goal = GoalScene.instantiate()
	add_child(goal)
	goal.position = Vector3(
		end_tile.x * Globals.GRID_SIZE,
		1,
		end_tile.y * Globals.GRID_SIZE
)


	map.free()
