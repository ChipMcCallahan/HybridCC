local Direction = {}

-- Define each direction as a table with x, y, z, and name.
Direction.N    = {x= 0, y=-1, z= 0, name="N"}
Direction.S    = {x= 0, y= 1, z= 0, name="S"}
Direction.E    = {x= 1, y= 0, z= 0, name="E"}
Direction.W    = {x=-1, y= 0, z= 0, name="W"}
Direction.UP   = {x= 0, y= 0, z= 1, name="U"}
Direction.DOWN = {x= 0, y= 0, z=-1, name="D"}

-- For quick name → direction table lookup
Direction._lookup = {}
for key, dir in pairs(Direction) do
    if type(dir) == "table" and dir.name then
        Direction._lookup[dir.name] = dir
    end
end

-- Simple direct maps for transformations
local right_map = {
    N = "E",  E = "S",  S = "W",  W = "N",
    U = "U",  D = "D"
}

local left_map = {
    N = "W",  W = "S",  S = "E",  E = "N",
    U = "U",  D = "D"
}

local reverse_map = {
    N = "S",  S = "N",  E = "W",  W = "E",
    U = "D",  D = "U"
}

-- Returns a direction table given its name, e.g. "N", "S", "U", etc.
function Direction.from_string(d_str)
    return Direction._lookup[d_str]
end

-- Check if direction is cardinal (N, E, S, W).
function Direction.is_cardinal(d)
    return (d.name == "N" or d.name == "E" or d.name == "S" or d.name == "W")
end

function Direction.right(d)  -- i.e. clockwise rotation
    local newName = right_map[d.name]
    return Direction._lookup[newName]
end

function Direction.reverse(d)
    local newName = reverse_map[d.name]
    return Direction._lookup[newName]
end

function Direction.left(d)  -- i.e. counter-clockwise rotation
    local newName = left_map[d.name]
    return Direction._lookup[newName]
end

-- Optional: detect direction by comparing two 3D points (old_p, new_p).
function Direction.from_move(old_p, new_p)
    local dx = new_p[1] - old_p[1]
    local dy = new_p[2] - old_p[2]
    local dz = new_p[3] - old_p[3]
    for _, dir in pairs(Direction._lookup) do
        if dir.x == dx and dir.y == dy and dir.z == dz then
            return dir
        end
    end
    return nil
end

return Direction
