# Worms cursor

An arrow cursor for the Omarchy shell. It turns to follow the pointer and keeps the last angle when the mouse stops.

The plugin draws the arrow on a click-through overlay. A blank Xcursor theme hides the system arrow underneath. Text and resize cursors still come from Adwaita.

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
```

```sh
mkdir -p ~/.local/share/icons
cp -a ~/.config/omarchy/plugins/otlet.worms-cursor/cursors/worms-cursor ~/.local/share/icons/
hyprctl setcursor worms-cursor 24
```

Hyprland reloads `looknfeel.lua` on save. New windows pick up the theme after `hyprctl setcursor`.

## Remove

```sh
omarchy plugin remove otlet.worms-cursor
rm -rf ~/.local/share/icons/worms-cursor
```

Delete the `hl.env("XCURSOR_THEME", "worms-cursor")` line and set your previous cursor theme. Leaving that line in place hides the arrow after the plugin is gone.

```sh
hyprctl setcursor Adwaita 24
```
