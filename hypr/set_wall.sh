#!/usr/bin/env bash
# WALLPAPER_DIR="$HOME/wallpapers/"
# CURRENT_WALL=$(hyprctl hyprpaper listloaded)
#
# # Get a random wallpaper that is not the current one
# WALLPAPER=$(find "$WALLPAPER_DIR" -type f ! -name "$(basename "$CURRENT_WALL")" | shuf -n 1)
#
# # Apply the selected wallpaper
# hyprctl hyprpaper reload ,"$WALLPAPER"

WALLPAPER_DIR="$HOME/Pictures/Wallpapers/" # Change this to your wallpaper directory
INTERVAL=100 # Set the interval in seconds (e.g., 900 for 15 minutes)

while true; do
  # Get a list of all wallpaper files
  WALLPAPERS=( "$WALLPAPER_DIR"*.{png,jpg,jpeg,webp} )

  # Choose a random wallpaper from the list
  RANDOM_WALLPAPER="${WALLPAPERS[$RANDOM % ${#WALLPAPERS[@]}]}"

  # Apply the wallpaper to all monitors
  hyprctl hyprpaper reload ,"$RANDOM_WALLPAPER"

  # Wait for the specified interval
  sleep "$INTERVAL"
done
