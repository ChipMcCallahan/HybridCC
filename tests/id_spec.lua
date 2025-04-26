local Id = require("shared.id")

describe("Id module", function()
  
  it("should have a _lookup table", function()
    assert.is_table(Id._lookup)
  end)

  it("should map the same references for each key", function()
    assert.is_not_nil(Id.SPACE)
    assert.is_not_nil(Id._lookup["SPACE"])
    assert.is_equal(Id.SPACE, Id._lookup["SPACE"], 
      "Id._lookup['SPACE'] should reference the same table as Id.SPACE")
  end)

  it("should contain the correct layer in each lookup", function()
    assert.equals(Id.SPACE.layer, Id._lookup["SPACE"].layer)
    assert.equals(Id.FLOOR.layer, Id._lookup["FLOOR"].layer)
  end)

end)
