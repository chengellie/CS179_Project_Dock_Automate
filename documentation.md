# Ship Operations/Search Documentation

## Classes

### Container

Member Variables
| Variable | Description |
| ------------------- | ------------------------- |
| manifest_coord | List with manifest version of coordinates, [x,y] |
| ship_coord | List with ship version of coordinates, [x,y] |
| ship_size | List with size of ship, [row, col] |
| weight | Container weight, int |
| name | Container name, str|

Member Functions
| Function | Description |
| ------------------- | ------------------------- |
| \_\_init\_\_ | Construct container |
| \_\_str\_\_ | Return 6-character shortened container name |
| get_manifest_format | Return formatted container for outbound manifest |
| get_shortened_name | Return 6-character shortened container name |
| set_manifest_coord | Update manifest and ship version of coordinates given new manifest coordinates |
| set_ship_coord | Update manifest and ship version of coordinates given new ship coordinates |

### Ship

Member Variables
| Variable | Description |
| ------------------- | ------------------------- |
| ship_state | 2D list of containers in ship, top left [0,0] |
| goal_state | Dictionary with desired containers and their counts |
| row | Number of rows in ship, initialized to 8 |
| col | Number of columns in ship, initialized to 12 |

Member Functions

| Function                     | Description                                             |
| ---------------------------- | ------------------------------------------------------- |
| \_\_init\_\_                 | Construct ship                                          |
| \_\_init_ship_state_manifest | Construct ship_state using manifest                     |
| \_\_init_ship_state_names    | Construct ship_state using container names              |
| \_\_init_goal_state          | Construct goal_state dictionary                         |
| \_\_str\_\_                  | Return grid representation for ship_state               |
| print_weights                | Print grid representation of container weights          |
| is_balanced                  | Test whether ship is balanced                           |
| is_goal_state                | Test whether current state is goal state                |
| get_outbound_manifest        | Return contents for outbound manifest                   |
| get_container_depth          | Return number of containers on top of a given container |

## Global Functions

### Ship Util

| Function  | Description                                                               |
| --------- | ------------------------------------------------------------------------- |
| get_moves | Return list of coordinates to move container from one position to another |
