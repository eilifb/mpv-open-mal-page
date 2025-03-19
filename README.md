# Open My Anime List Page
![image](banner.jpg)

Simple mpv script that uses [GuessIt](https://pypi.org/project/guessit/) to
make a query to the [My Anime List API](https://myanimelist.net/apiconfig/references/api/v2)
and opens up the corresponding MAL webpage if a match is found. Inspired by [ctlaltdefeat's Open IMDb Page Script](https://github.com/ctlaltdefeat/mpv-open-imdb-page).
The script takes (part of) the filepath and queries MAL, and then makes a comparison
between filepath and titles of the shows/movies returned by MAL. If  the similarity is over a given threshold it opens a tab to MAL.

See [Configuration](#conf) for options.

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

<a name="conf" />

## Configuration

All configuration options are set via `/scrip-opts/open-mal-page.conf`
#### python **Required!**
- Path to your python installation. You can get the path to your python installation with `(get-command python).Path` on Windows, or `which python3` on OSX/Linux

#### mal_id **Required!**
- Your My Anime List Client ID. You need a MAL profile, and can generate it at your profile's [API panel](https://myanimelist.net/apiconfig).

#### title_threshold
- How similar the title GuessIt finds has to be to title(s) returned by MAL.
Setting this to `1.00` means that the title has to be a exact match, while setting it to `0.00` means that it will match
with the first result returned by MAL. MAL's query is quite lenient, so `0.00` will almost always return *something*.
- Note that `GuessIt` can sometimes remove characters from the filepath that actually belong to the title, so I don't recommend setting `title_threshold=1.00`.

    E.G. `guessit "C:\Anime\[DVD_ISO] Blue Submarine No. 6 (US)\Episode 01.mkv"` will return the title `Blue Submarine No 6` (missing `.`), and thus not exactly match the title stored in MAL's database.
- The default value is `title_threshold=0.80`, which seems to work well. But feel free to experiment.
- Some examples:
    - *Blue Submarine No 6* and *Blue Submarine No. 6* gives a **0.974** match
    - *Trapeze* and *Trapezium* gives a **0.75** match
    - *yu-gi-oh gx* and *Yugioh GX* gives a **0.600** match
    - *yu-gi-oh gx* and * Yu☆Gi☆Oh! Duel Monsters GX* gives a **0.216** match

#### debug
- Makes the script output quite a lot of text that may or may not be helpful/make sense
- Default is `debug=no`

## TODO
- [ ] Confirm Linux/OSX compatability (Can't see why it shouldn't)
- [ ] Write a installation guide for Linux/OSX
- [ ] Figure out why I went with MAL's API instead of [Jikan](https://jikan.moe/)