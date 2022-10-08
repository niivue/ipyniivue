from traitlets import TraitType
import enum

class Volume(TraitType):
	default_value = {}
	info_text = 'a volume'

	def validate(self, obj, value):
		accepted_keys = {'url', 'volume', 'name', 'color_map', 'opacity', 'visible'}
		if isinstance(value, dict):
			if len(value.keys()-accepted_keys) == 0:
				return value
		self.error(obj, value)

class DragModes(int, enum.Enum):
    none = 0
    contrast = 1
    measurement = 2
    pan = 3

#https://www.freecodecamp.org/news/javascript-keycode-list-keypress-event-key-codes/
keycodes = ['Backspace', 'Tab', 'Enter', 'ShiftLeft', 'ShiftRight', 'ControlLeft', 'ControlRight', 'AltLeft', 'AltRight', 'Pause', 'CapsLock', 'Escape', 'Space', 'PageUp', 'PageDown', 'End', 'Home', 'ArrowLeft', 'ArrowUp', 'ArrowRight', 'ArrowDown', 'PrintScreen', 'Insert', 'Delete', 'Digit0', 'Digit1', 'Digit2', 'Digit3', 'Digit4', 'Digit5', 'Digit6', 'Digit7', 'Digit8', 'Digit9', 'KeyA', 'KeyB', 'KeyC', 'KeyD', 'KeyE', 'KeyF', 'KeyG', 'KeyH', 'KeyI', 'KeyJ', 'KeyK', 'KeyL', 'KeyM', 'KeyN', 'KeyO', 'KeyP', 'KeyQ', 'KeyR', 'KeyS', 'KeyT', 'KeyU', 'KeyV', 'KeyW', 'KeyX', 'KeyY', 'KeyZ', 'MetaLeft', 'MetaRight', 'ContextMenu', 'Numpad0', 'Numpad1', 'Numpad2', 'Numpad3', 'Numpad4', 'Numpad5', 'Numpad6', 'Numpad7', 'Numpad8', 'Numpad9', 'NumpadMultiply', 'NumpadAdd', 'NumpadSubtract', 'NumpadDecimal', 'NumpadDivide', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12', 'NumLock', 'ScrollLock', 'Semicolon', 'Equal', 'Comma', 'Minus', 'Period', 'Slash', 'Backquote', 'BracketLeft', 'Backslash', 'BracketRight', 'Quote']