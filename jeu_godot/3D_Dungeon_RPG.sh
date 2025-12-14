#!/bin/sh
printf '\033c\033]0;%s\a' 3D Dungeon RPG
base_path="$(dirname "$(realpath "$0")")"
"$base_path/3D_Dungeon_RPG.x86_64" "$@"
