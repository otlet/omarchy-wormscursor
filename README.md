# Worms cursor

An arrow cursor for the Omarchy shell. It turns to follow the pointer and keeps the last angle when the mouse stops.

The plugin draws the arrow on a click-through overlay. Apps send their own text caret and hand, so the system cursor has to be hidden entirely. A blank Xcursor theme covers the shapes Hyprland loads itself.

## Dependencies

- Omarchy with Hyprland and the Quattro shell
- `python3` from the base system

No extra packages. The plugin does not change your configuration by itself.

## Install

```sh
omarchy plugin add https://github.com/otlet/omarchy-wormscursor.git --enable
```

Copy the blank cursor theme, then point Hyprland at it. In `~/.config/hypr/looknfeel.lua`:

```lua
hl.env("XCURSOR_THEME", "worms-cursor")
hl.config({
  cursor = {
    invisible = true,
  },
})
```

```sh
python3 ~/.config/omarchy/plugins/otlet.worms-cursor/blank_cursor.py
mkdir -p ~/.local/share/icons
cp -a ~/.config/omarchy/plugins/otlet.worms-cursor/cursors/worms-cursor ~/.local/share/icons/
# Same theme and size is a no-op. Change the size once so Hyprland rescans.
hyprctl setcursor worms-cursor 48
hyprctl setcursor worms-cursor 24
```

Hyprland reloads `looknfeel.lua` on save. `cursor.invisible` hides every system cursor, including resize. The worm stays.

## Development

```sh
uv sync --extra dev
uv run pytest -q
uv run ruff check .
```

Conventional commits are enforced by commitizen (commit-msg hook). Convenient commit:

```sh
./scripts/commit.sh -m "feat: ..."
# or
make commit
```

## Remove

```sh
omarchy plugin remove otlet.worms-cursor
rm -rf ~/.local/share/icons/worms-cursor
```

Delete the `XCURSOR_THEME` and `cursor.invisible` lines, then set your previous cursor theme. Leaving them in place hides the cursor after the plugin is gone.

```sh
hyprctl setcursor Adwaita 24
```
