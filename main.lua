local mp = require('mp')
local utils = require('mp.utils')
local mpopt = require('mp.options')

local config = {
    subliminal = "",
    mal_id = "",
    debug = false
}

local function log_debug(input, secs)
    if not config.debug then
        return
    end
    local traceback = debug.traceback()
    local iterator = traceback:gmatch("[^\n]+")
    local current = iterator()
    local next_match = ""
    while current do
        next_match = iterator()
        if current:match("log_debug") then
            break
        end
        current = next_match
    end
    input = tostring(input)
    next_match = next_match:gsub(".*/", "")
    mp.msg.warn(input .. " | file:line  - " .. next_match)
end


local function init()
    mpopt.read_options(config, "open-mal-page")

    log_debug(config.subliminal)
    log_debug(config.mal_id)

    if utils.file_info(config.subliminal) == nil then
        mp.msg.error("subliminal path not found!")
        mp.osd_message("ERROR: open-mal-page - Subliminal not found!")
        return
    end


    log_debug("open-mal-page finished!")
end

init()
