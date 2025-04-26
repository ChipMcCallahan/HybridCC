local Enums = {}

Enums.BombRule = {
    STARTS_ARMED = 0,
    STARTS_DISARMED = 1
}

Enums.ButtonRule = {
    TOGGLE = 1,
    HOLD_ONE = 2,
    HOLD_ALL = 3,
    DPAD = 4
}

Enums.Color = {
    GREY    = "#CCCCCC",
    RED     = "#FF0000",
    GREEN   = "#008000",
    BLUE    = "#2222FF",
    YELLOW  = "#FFFF00",
    MAGENTA = "#FF00FF",
    CYAN    = "#00FFFF",
    ORANGE  = "#FF8C00",
    BROWN   = "#4B3619"
}

Enums.ForceRule = {
    DEFAULT = 1,
    RANDOM  = 2
}

Enums.KeyRule = {
    DEFAULT     = 1,
    FRAGILE     = 2,
    ACTING_DIRT = 3
}

Enums.Layer = {
    UNKNOWN     = 0,
    TERRAIN     = 1,
    TERRAIN_MOD = 2,
    PICKUP      = 3,
    MOB         = 4,
    SIDES       = 5
}

Enums.MonsterRule = {
    TEETH       = 1,
    BLOB        = 2,
    FIREBALL    = 3,
    GLIDER      = 4,
    ANT         = 5,
    PARAMECIUM  = 6,
    BALL        = 7,
    WALKER      = 8
}

Enums.MoveResult = {
    PASS  = 1,
    FAIL  = 2,
    RETRY = 3,
    DEFER = 4
}

Enums.SpaceRule = {
    DEFAULT            = 1,
    SOLID_BELOW        = 2,
    MAYBE_SOLID_BELOW  = 3,
    DEADLY_BELOW       = 4
}

Enums.SteppingStoneRule = {
    WATER = 0,
    FIRE  = 1,
    ICE   = 2
}

Enums.ThiefRule = {
    TOOLS = 0,
    KEYS  = 1
}

Enums.ToggleWallRule = {
    STARTS_OPEN = 0,
    STARTS_SHUT = 1
}

-- TODO: combine with Key Rule. Should be
-- Default, Fragile, Item Barrier, Gift (so monsters and blocks can use)
Enums.ToolRule = {
    DEFAULT       = 0,
    ITEM_BARRIER  = 1
}

Enums.TrapRule = {
    STARTS_OPEN = 0,
    STARTS_SHUT = 1
}

Enums.TrickWallRule = {
    PERMANENTLY_INVISIBLE  = 1,
    INVISIBLE_BECOMES_WALL = 2,
    BECOMES_FLOOR          = 3,
    BECOMES_WALL           = 4,
    PASS_THRU              = 5,
    SOLID                  = 6
}

Enums.Tag = {
    -- Temporary tags
    PUSHING      = "pushing",
    PUSHED       = "pushed",
    SWIMMING     = "swimming",
    RETRY_MOVE   = "retry_move",
    FAILED_MOVE  = "failed_move",
    MOVED        = "moved",
    SLIDING      = "sliding",
    FORCED       = "forced",
    OVERRIDDEN   = "overridden",
    TRAPPED      = "trapped",
    SPEED_BOOST  = "speed_boost",

    -- Permanent tags or traits
    COLLECTS_CHIPS   = "collects_chips",
    COLLECTS_ITEMS   = "collects_items",
    ENTERS_DIRT      = "enters_dirt",
    PUSHABLE         = "pushable",
    PUSHES           = "pushes"
}

return Enums
