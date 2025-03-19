local mp = require('mp')
local utils = require('mp.utils')
local mpopt = require('mp.options')

local config = {
    python = "",
    mal_id = "",
    title_threshold = "0.55",
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

    if utils.file_info(config.python) == nil then
        mp.msg.error("python path not found!")
        mp.osd_message("ERROR: open-mal-page - Python path not found!")
        return
    end

    if config.mal_id == "" then
        mp.msg.error("MAL Client ID not supplied")
        mp.osd_message("ERROR: open-mal-page - Need MAL Client ID!")
        return
    end



    local python_call = {
        config.python,
        mp.get_script_directory().."/open_mal_page.py",
        mp.get_property("path"),
        config.mal_id,
        config.title_threshold
    }

    log_debug("python_call: "..utils.to_string(python_call))

    mp.osd_message("querying MAL...", 30)
    mp.msg.warn("Searching... (running python script)")

    local output = mp.command_native {
        name = "subprocess",
        playback_only = false,
        capture_stdout = true,
        args = python_call
    }


    if config.debug then
        for line in string.gmatch(output["stdout"], "(.-)\n") do
            mp.msg.warn("Python: "..line)
        end
    end

    if output["status"] == 0 then
        mp.osd_message("Found match! Opening page...")
        mp.msg.warn("Found match! Opening page...")
    elseif output["status"] == 1 then
        mp.osd_message("Found no match.")
        mp.msg.warn("Found no match.")
    elseif output["status"] == 2 then
        mp.osd_message("Got unexpected respnse from MAL")
        mp.msg.warn("Got unexpected respnse from MAL")
    elseif output["status"] == 3 then
        mp.osd_message("Found no match with exact title.")
        mp.msg.warn("Found no match with exact title.")
    end

    log_debug("open-mal-page finished!")
end

mp.add_key_binding('Alt+m', 'open_mal_page', Open_mal_page)
