local mp = require('mp')
local utils = require('mp.utils')
local mpopt = require('mp.options')

local config = {
    python = "",
    mal_key = ""
}


local function init()
    mpopt.read_options(config, "open-mal-page")
end

init()
