-- Unit tests for direction.lua using the Busted testing framework.
-- Run on CLI with '$ busted'

describe("Direction module", function()
    local Direction = require("shared.direction")

    describe("from_string", function()
        it("returns correct direction for N, S, E, W, U, D", function()
            local dN = Direction.from_string("N")
            assert.is_not_nil(dN)
            assert.is_equal(dN.name, "N")
            assert.is_equal(dN.x, 0)
            assert.is_equal(dN.y, -1)
            assert.is_equal(dN.z, 0)

            local dS = Direction.from_string("S")
            assert.is_not_nil(dS)
            assert.is_equal(dS.name, "S")

            local dE = Direction.from_string("E")
            assert.is_not_nil(dE)
            assert.is_equal(dE.name, "E")

            local dW = Direction.from_string("W")
            assert.is_not_nil(dW)
            assert.is_equal(dW.name, "W")

            local dU = Direction.from_string("U")
            assert.is_not_nil(dU)
            assert.is_equal(dU.name, "U")

            local dD = Direction.from_string("D")
            assert.is_not_nil(dD)
            assert.is_equal(dD.name, "D")
        end)

        it("returns nil for unknown string", function()
            local dX = Direction.from_string("X")
            assert.is_nil(dX)
        end)
    end)

    describe("is_cardinal", function()
        it("returns true for N, E, S, W", function()
            assert.is_true(Direction.is_cardinal(Direction.N))
            assert.is_true(Direction.is_cardinal(Direction.E))
            assert.is_true(Direction.is_cardinal(Direction.S))
            assert.is_true(Direction.is_cardinal(Direction.W))
        end)

        it("returns false for UP, DOWN", function()
            assert.is_false(Direction.is_cardinal(Direction.UP))
            assert.is_false(Direction.is_cardinal(Direction.DOWN))
        end)
    end)

    describe("right", function()
        it("rotates cardinal directions clockwise", function()
            -- N -> E, E -> S, S -> W, W -> N
            assert.is_equal(Direction.right(Direction.N).name, "E")
            assert.is_equal(Direction.right(Direction.E).name, "S")
            assert.is_equal(Direction.right(Direction.S).name, "W")
            assert.is_equal(Direction.right(Direction.W).name, "N")
        end)

        it("keeps UP and DOWN the same", function()
            assert.is_equal(Direction.right(Direction.UP), Direction.UP)
            assert.is_equal(Direction.right(Direction.DOWN), Direction.DOWN)
        end)
    end)

    describe("reverse", function()
        it("reverses cardinal directions", function()
            -- N -> S, E -> W, S -> N, W -> E
            assert.is_equal(Direction.reverse(Direction.N).name, "S")
            assert.is_equal(Direction.reverse(Direction.S).name, "N")
            assert.is_equal(Direction.reverse(Direction.E).name, "W")
            assert.is_equal(Direction.reverse(Direction.W).name, "E")
        end)

        it("flips UP <-> DOWN", function()
            assert.is_equal(Direction.reverse(Direction.UP), Direction.DOWN)
            assert.is_equal(Direction.reverse(Direction.DOWN), Direction.UP)
        end)
    end)

    describe("left", function()
        it("rotates cardinal directions counterclockwise", function()
            -- N -> W, W -> S, S -> E, E -> N
            assert.is_equal(Direction.left(Direction.N).name, "W")
            assert.is_equal(Direction.left(Direction.W).name, "S")
            assert.is_equal(Direction.left(Direction.S).name, "E")
            assert.is_equal(Direction.left(Direction.E).name, "N")
        end)

        it("keeps UP and DOWN the same", function()
            assert.is_equal(Direction.left(Direction.UP), Direction.UP)
            assert.is_equal(Direction.left(Direction.DOWN), Direction.DOWN)
        end)
    end)

    describe("from_move", function()
        it("returns correct direction from two points", function()
            -- old_p: (0,0,0), new_p: (0,-1,0) => N
            local dN = Direction.from_move({0,0,0}, {0,-1,0})
            assert.is_not_nil(dN)
            assert.is_equal(dN.name, "N")

            -- E
            local dE = Direction.from_move({0,0,0}, {1,0,0})
            assert.is_not_nil(dE)
            assert.is_equal(dE.name, "E")

            -- S
            local dS = Direction.from_move({3,5,0}, {3,6,0})
            assert.is_not_nil(dS)
            assert.is_equal(dS.name, "S")

            -- W
            local dW = Direction.from_move({2,2,2}, {1,2,2})
            assert.is_not_nil(dW)
            assert.is_equal(dW.name, "W")

            -- UP
            local dU = Direction.from_move({1,1,1}, {1,1,2})
            assert.is_not_nil(dU)
            assert.is_equal(dU.name, "U")

            -- DOWN
            local dDown = Direction.from_move({2,2,2}, {2,2,1})
            assert.is_not_nil(dDown)
            assert.is_equal(dDown.name, "D")
        end)

        it("returns nil if the change doesn't match a known direction", function()
            -- e.g. diagonal or something else
            local dUnknown = Direction.from_move({0,0,0}, {1,1,0})
            assert.is_nil(dUnknown)
        end)
    end)
end)
