#[allow(dead_code)]
extern crate serde_json;
use early_returns::some_or_return;
use gilrs::{Axis, Button, Gamepad};
use serde::Serialize;
use std::collections::HashMap;

#[derive(Debug, Serialize)]
pub struct GamepadData {
    buttons: HashMap<String, bool>,
    left_stick: (f32, f32),
    right_stick: (f32, f32),
    dpad: (i8, i8),
}

impl GamepadData {
    pub fn new(gamepad: Gamepad) -> GamepadData {
        let buttons = GamepadData::get_buttons(gamepad);
        let left_stick = GamepadData::get_left_stick(gamepad);
        let right_stick = GamepadData::get_right_stick(gamepad);
        let dpad = GamepadData::get_dpad(gamepad);

        GamepadData {
            buttons,
            left_stick,
            right_stick,
            dpad,
        }
    }

    pub fn get_buttons(gamepad: Gamepad) -> HashMap<String, bool> {
        let mut buttons: HashMap<String, bool> = HashMap::new();

        buttons.insert("North".to_string(), gamepad.is_pressed(Button::North));
        buttons.insert("East".to_string(), gamepad.is_pressed(Button::East));
        buttons.insert("South".to_string(), gamepad.is_pressed(Button::South));
        buttons.insert("West".to_string(), gamepad.is_pressed(Button::West));
        buttons.insert(
            "Left Bumper".to_string(),
            gamepad.is_pressed(Button::LeftTrigger),
        );
        buttons.insert(
            "Right Bumper".to_string(),
            gamepad.is_pressed(Button::RightTrigger),
        );
        buttons.insert(
            "Left Trigger".to_string(),
            gamepad.is_pressed(Button::LeftTrigger2),
        );
        buttons.insert(
            "Right Trigger".to_string(),
            gamepad.is_pressed(Button::RightTrigger2),
        );
        buttons.insert(
            "Left Thumb".to_string(),
            gamepad.is_pressed(Button::LeftThumb),
        );
        buttons.insert(
            "Right Thumb".to_string(),
            gamepad.is_pressed(Button::RightThumb),
        );
        buttons.insert("Start".to_string(), gamepad.is_pressed(Button::Start));
        buttons.insert("Select".to_string(), gamepad.is_pressed(Button::Select));
        buttons
    }

    pub fn get_left_stick(gamepad: Gamepad) -> (f32, f32) {
        (
            get_filtered_axis(gamepad, Axis::LeftStickX),
            get_filtered_axis(gamepad, Axis::LeftStickY),
        )
    }
    pub fn get_right_stick(gamepad: Gamepad) -> (f32, f32) {
        (
            get_filtered_axis(gamepad, Axis::RightStickX),
            get_filtered_axis(gamepad, Axis::RightStickY),
        )
    }

    pub fn get_dpad(gamepad: Gamepad) -> (i8, i8) {
        let dpad_x = if gamepad.is_pressed(Button::DPadLeft) {
            -1
        } else if gamepad.is_pressed(Button::DPadRight) {
            1
        } else {
            0
        };

        let dpad_y = if gamepad.is_pressed(Button::DPadDown) {
            -1
        } else if gamepad.is_pressed(Button::DPadUp) {
            1
        } else {
            0
        };
        (dpad_x, dpad_y)
    }
}

fn get_filtered_axis(gamepad: Gamepad, axis: Axis) -> f32 {
    let axis_code = some_or_return!(gamepad.axis_code(axis), 0.0);
    let deadzone = some_or_return!(gamepad.deadzone(axis_code), 0.0);
    let axis_value = gamepad.value(axis);

    if axis_value.abs() < deadzone {
        return 0.0;
    } else {
        return axis_value;
    }
}
