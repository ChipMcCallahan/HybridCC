-- shared/id.lua
-- We include a lookup table so we can find entries by their key.

local Enums = require("shared.enums")
local Layer = Enums.Layer

local Id = {}

-- === 1) Define All IDs ===
Id.DEFAULT         = { layer = Layer.UNKNOWN }

Id.SPACE           = { layer = Layer.TERRAIN }
Id.FLOOR           = { layer = Layer.TERRAIN }
Id.WALL            = { layer = Layer.TERRAIN }
Id.EXIT            = { layer = Layer.TERRAIN }
Id.WATER           = { layer = Layer.TERRAIN }
Id.FIRE            = { layer = Layer.TERRAIN }
Id.TRICK_WALL      = { layer = Layer.TERRAIN }
Id.DIRT            = { layer = Layer.TERRAIN }
Id.ICE             = { layer = Layer.TERRAIN }
Id.FORCE           = { layer = Layer.TERRAIN }
Id.TELEPORT        = { layer = Layer.TERRAIN }
Id.TRAP            = { layer = Layer.TERRAIN }
Id.GRAVEL          = { layer = Layer.TERRAIN }
Id.POP_UP_WALL     = { layer = Layer.TERRAIN }
Id.STEPPING_STONE  = { layer = Layer.TERRAIN }
Id.HINT            = { layer = Layer.TERRAIN }
Id.CLONER          = { layer = Layer.TERRAIN }
Id.THIEF           = { layer = Layer.TERRAIN }

Id.DOOR            = { layer = Layer.TERRAIN_MOD }
Id.SOCKET          = { layer = Layer.TERRAIN_MOD }
Id.BUTTON          = { layer = Layer.TERRAIN_MOD }
Id.TOGGLE_WALL     = { layer = Layer.TERRAIN_MOD }

Id.CHIP            = { layer = Layer.PICKUP }
Id.BOMB            = { layer = Layer.PICKUP }
Id.KEY             = { layer = Layer.PICKUP }
Id.FLIPPERS        = { layer = Layer.PICKUP }
Id.FIRE_BOOTS      = { layer = Layer.PICKUP }
Id.SKATES          = { layer = Layer.PICKUP }
Id.SUCTION_BOOTS   = { layer = Layer.PICKUP }

Id.PANEL           = { layer = Layer.SIDES }
Id.CORNER          = { layer = Layer.SIDES }

Id.DIRT_BLOCK      = { layer = Layer.MOB }
Id.ICE_BLOCK       = { layer = Layer.MOB }
Id.MONSTER         = { layer = Layer.MOB }
Id.TANK            = { layer = Layer.MOB }
Id.ROBOT           = { layer = Layer.MOB }
Id.PLAYER          = { layer = Layer.MOB }
Id.PLACEHOLDER     = { layer = Layer.MOB }

-- === 2) Build a lookup table so we can find entries by their 'name' (the key). ===
Id._lookup = {}
for key, value in pairs(Id) do
    if type(value) == "table" and value.layer then
        -- Use the key as the name to reference this entry in the lookup
        Id._lookup[key] = value
    end
end

return Id
