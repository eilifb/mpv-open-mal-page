# Open My Anime List Page
![image](banner.jpg)

Simple mpv script that uses [GuessIt](https://pypi.org/project/guessit/) to
make a query to the [My Anime List API](https://myanimelist.net/apiconfig/references/api/v2)
and opens up the corresponding MAL webpage if a match is found.

The Python script can be used on its own if you want to do that for some reason.

## Requirements
- [Python](https://www.python.org/downloads/)
- [GuessIt](https://pypi.org/project/guessit/)
- [MAL Client ID](https://help.myanimelist.net/hc/en-us/articles/900003108823-API)

## Installation
### Windows:
- Locate either your mpv config folder, usually in `C:\Users\[USER]\AppData\Local\mpv`
or create a portable config in your mpv installation, e.g. `C:\Program Files\mpv\portable_config`
- Create a folder `scripts` in your config folder, e.g `\mpv\scripts` or `\portable_config\scripts`
- Create a folder `script-opts` in your config folder, e.g `\mpv\script-opts` or `\portable_config\script-opts`
- [Download this script](https://github.com/eilifb/mpv-open-mal-page/archive/refs/heads/main.zip) and extract the folder so that the structure is
`\mpv\scripts\mpv-open-mal-page-main` or `portable_config\scripts\mpv-open-mal-page-main`
- Move the `\open-mal-page_example_conf` from `\scripts\mpv-open-mal-page-main` to `\script-opts`, and rename it to `open-mal-page.conf`
- Replace the placeholder option values for your Python path (Hint: `(get-command python).Path` on Windows) and MAL Client ID
- Open a episode or movie with mpv and press __Alt+m__
- Optional: Replace __Alt+m__ with your prefered \[hotkey\] by adding the line `[hotkey] script-binding open_mal_page` to your [`input.conf`](https://mpv.io/manual/master/#input-conf) file

Powershell:
```powershell
pip install guessit
cd C:\Users\[USER]\AppData\Local\mpv
mkdir scripts # If folder does not exists already
mkdir script-opts # If folder does not exists already
cd scripts
git clone https://github.com/eilifb/mpv-open-mal-page
mv mpv-open-mal-page\open-mal-page_example.conf ..\script-opts\open-mal-page.conf
```
Replace the placeholders, cant be bothered to do that in powershell.
### Linux/OSX:
Coming soon ™

Should be pretty easy to set up yourself though.
## TODO
- [ ] Confirm Linux/OSX compatability (Can't see why it shouldn't)
- [ ] Write a installation guide for Linux/OSX
- [ ] Figure out why I went with MAL's API instead of [Jikan](https://jikan.moe/)