import QtQuick
import Quickshell
import Quickshell.Io
import Quickshell.Wayland

// Blank XCursor underneath. This layer draws the arrow; the tip is the hotspot.
// shortcut: arrow stays visible while typing; Hyprland has no hide event to follow.
Item {
  id: root

  property real px: 0
  property real py: 0
  property real deg: 0
  property bool ready: false

  function note(line) {
    var parts = String(line).trim().split(" ")
    if (parts.length !== 3) return
    var x = parseFloat(parts[0])
    var y = parseFloat(parts[1])
    var d = parseFloat(parts[2])
    if (isNaN(x) || isNaN(y) || isNaN(d)) return
    root.px = x
    root.py = y
    root.deg = d
    root.ready = true
  }

  Process {
    id: watch
    running: true
    command: ["python3", "-u", Quickshell.env("HOME") + "/.config/omarchy/plugins/otlet.worms-cursor/watch.py"]
    stdout: SplitParser {
      onRead: function(line) { root.note(line) }
    }
    onExited: restart.restart()
  }

  Timer {
    id: restart
    interval: 400
    onTriggered: watch.running = true
  }

  Variants {
    model: Quickshell.screens

    PanelWindow {
      id: panel
      required property var modelData
      screen: modelData
      anchors { top: true; bottom: true; left: true; right: true }
      color: "transparent"
      exclusionMode: ExclusionMode.Ignore
      WlrLayershell.namespace: "otlet-worms-cursor"
      WlrLayershell.layer: WlrLayer.Overlay
      WlrLayershell.keyboardFocus: WlrKeyboardFocus.None
      mask: Region {}

      Item {
        readonly property real lx: root.px - panel.screen.x
        readonly property real ly: root.py - panel.screen.y
        visible: root.ready && lx > -48 && ly > -48 && lx < panel.screen.width + 48 && ly < panel.screen.height + 48
        x: lx
        y: ly
        transformOrigin: Item.TopLeft
        rotation: root.deg

        // Tip is (48, 24) in the canvas, which is (0, 0) on this item.
        // Canvas, not Shape: the curve renderer paints a green rectangle on this layer.
        Canvas {
          x: -48
          y: -24
          width: 96
          height: 48
          antialiasing: true
          Component.onCompleted: requestPaint()
          onPaint: {
            var c = getContext("2d")
            c.clearRect(0, 0, width, height)
            c.beginPath()
            c.moveTo(48, 24)
            c.lineTo(20, 6)
            c.lineTo(20, 18)
            c.lineTo(4, 18)
            c.lineTo(4, 30)
            c.lineTo(20, 30)
            c.lineTo(20, 42)
            c.closePath()
            c.fillStyle = "#ffffff"
            c.strokeStyle = "#000000"
            c.lineWidth = 3
            c.lineJoin = "round"
            c.fill()
            c.stroke()
          }
        }
      }
    }
  }
}
