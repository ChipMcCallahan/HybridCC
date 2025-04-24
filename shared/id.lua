-- shared/id.lua
-- A Lua adaptation of the Id enum, omitting the numeric index.
-- Each entry has { name = "...", layer = <Layer constant> }.

local Layer = require("shared.enums")

local Id = {}

-- === 1) Define All IDs ===
Id.DEFAULT         = { name = "DEFAULT",         layer = Layer.UNKNOWN }

Id.SPACE           = { name = "SPACE",           layer = Layer.TERRAIN }
Id.FLOOR           = { name = "FLOOR",           layer = Layer.TERRAIN }
Id.WALL            = { name = "WALL",            layer = Layer.TERRAIN }
Id.EXIT            = { name = "EXIT",            layer = Layer.TERRAIN }
Id.WATER           = { name = "WATER",           layer = Layer.TERRAIN }
Id.FIRE            = { name = "FIRE",            layer = Layer.TERRAIN }
Id.TRICK_WALL      = { name = "TRICK_WALL",      layer = Layer.TERRAIN }
Id.DIRT            = { name = "DIRT",            layer = Layer.TERRAIN }
Id.ICE             = { name = "ICE",             layer = Layer.TERRAIN }
Id.FORCE           = { name = "FORCE",           layer = Layer.TERRAIN }
Id.TELEPORT        = { name = "TELEPORT",        layer = Layer.TERRAIN }
Id.TRAP            = { name = "TRAP",            layer = Layer.TERRAIN }
Id.GRAVEL          = { name = "GRAVEL",          layer = Layer.TERRAIN }
Id.POP_UP_WALL     = { name = "POP_UP_WALL",     layer = Layer.TERRAIN }
Id.STEPPING_STONE  = { name = "STEPPING_STONE",  layer = Layer.TERRAIN }
Id.HINT            = { name = "HINT",            layer = Layer.TERRAIN }
Id.CLONER          = { name = "CLONER",          layer = Layer.TERRAIN }
Id.THIEF           = { name = "THIEF",           layer = Layer.TERRAIN }

Id.DOOR            = { name = "DOOR",            layer = Layer.TERRAIN_MOD }
Id.SOCKET          = { name = "SOCKET",          layer = Layer.TERRAIN_MOD }
Id.BUTTON          = { name = "BUTTON",          layer = Layer.TERRAIN_MOD }
Id.TOGGLE_WALL     = { name = "TOGGLE_WALL",     layer = Layer.TERRAIN_MOD }

Id.CHIP            = { name = "CHIP",            layer = Layer.PICKUP }
Id.BOMB            = { name = "BOMB",            layer = Layer.PICKUP }
Id.KEY             = { name = "KEY",             layer = Layer.PICKUP }
Id.FLIPPERS        = { name = "FLIPPERS",        layer = Layer.PICKUP }
Id.FIRE_BOOTS      = { name = "FIRE_BOOTS",      layer = Layer.PICKUP }
Id.SKATES          = { name = "SKATES",          layer = Layer.PICKUP }
Id.SUCTION_BOOTS   = { name = "SUCTION_BOOTS",   layer = Layer.PICKUP }

Id.PANEL           = { name = "PANEL",           layer = Layer.SIDES }
Id.CORNER          = { name = "CORNER",          layer = Layer.SIDES }

Id.DIRT_BLOCK      = { name = "DIRT_BLOCK",      layer = Layer.MOB }
Id.ICE_BLOCK       = { name = "ICE_BLOCK",       layer = Layer.MOB }
Id.MONSTER         = { name = "MONSTER",         layer = Layer.MOB }
Id.TANK            = { name = "TANK",            layer = Layer.MOB }
Id.ROBOT           = { name = "ROBOT",           layer = Layer.MOB }
Id.PLAYER          = { name = "PLAYER",          layer = Layer.MOB }
Id.PLACEHOLDER     = { name = "PLACEHOLDER",     layer = Layer.MOB }

-- === 2) Build a lookup table so we can find entries by their name string. ===
Id._lookup = {}
for k, v in pairs(Id) do
    if type(v) == "table" and v.name then
        Id._lookup[v.name] = v
    end
end

return Id
