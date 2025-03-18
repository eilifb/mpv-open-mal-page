local mp = require('mp')
local utils = require('mp.utils')
local mpopt = require('mp.options')

local config = {
    python = "",
    mal_id = "",
    debug = false
}

local function log_debug(input)
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


function Open_mal_page()
    mpopt.read_options(config, "open-mal-page")

    log_debug(config.python)
    log_debug(config.mal_id)

    if utils.file_info(config.python) == nil then
        mp.msg.error("python path not found!")
        mp.osd_message("ERROR: open-mal-page - Subliminal not found!")
        return
    end


    local filepath = mp.get_property("path")
    log_debug("filepath: "..filepath)
    local args = {
        config.python,
        mp.get_script_directory().."/open_mal_page.py",
        filepath
    }

    log_debug("args: "..utils.to_string(args))

    local output = mp.command_native {
        name = "subprocess",
        playback_only = false,
        capture_stdout = true,
        args = args
    }

    if config.debug then
        for line in string.gmatch(output["stdout"], "(.-)\n") do
            mp.msg.warn("Python: "..line)
        end
    end
    log_debug("open-mal-page finished!")
end

mp.add_key_binding('ø', 'open_mal_page', Open_mal_page)
