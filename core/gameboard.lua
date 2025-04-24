-- core/gameboard.lua
-- A stub for the "GameBoard" object with a do_logic method that mimics
-- the Python logic snippet you provided.

local Direction = require("shared.direction")

local GameBoard = {}
GameBoard.__index = GameBoard

-- Simple constructor
function GameBoard.new()
    local self = setmetatable({}, GameBoard)
    -- Any other initialization goes here
    return self
end

-- do_logic stub
function GameBoard:do_logic(inputs)
    -- Convert string inputs to Direction tables if needed
    for i = 1, #inputs do
        if type(inputs[i]) == "string" then
            inputs[i] = Direction.from_string(inputs[i])
        end
    end

    -- pop function to remove first element
    local function pop()
        if #inputs > 0 then
            return table.remove(inputs, 1)
        end
        return nil
    end

    local i1 = pop()
    local i2 = nil

    -- The Python logic: while inputs and i1 and not i2,
    -- if the next direction is i1.right() or i1.left(), we pick it as i2
    while (#inputs > 0) and i1 and (not i2) do
        local d = pop()
        if d == Direction.right(i1) or d == Direction.left(i1) then
            i2 = d
        end
    end

    local final = {i1, i2}

    -- For now, just log/print them
    print("GameBoard.do_logic final inputs:", 
          final[1] and final[1].name or "nil", 
          final[2] and final[2].name or "nil")
end

return GameBoard
