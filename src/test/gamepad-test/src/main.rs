#[allow(dead_code)]
use anyhow::Result;
use serde::Serialize;
use std::collections::HashMap;
use std::time::Duration;
use std::thread;
use gilrs::{Axis, Button, GamepadId, Gilrs};

#[derive(Debug, Serialize)]
struct JoystickValues {
    buttons: HashMap<String, bool>,
    left_stick: (f32, f32),
    right_stick: (f32, f32),
    dpad: (i8, i8),
}

impl JoystickValues {
    pub fn new(buttons: HashMap<String, bool>, left_stick: (f32, f32), right_stick: (f32, f32), dpad: (i8, i8)) -> JoystickValues {
        JoystickValues {
            buttons,
            left_stick,
            right_stick,
            dpad
        }
    } 
}


fn main() -> Result<()> {
    let mut gilrs: Gilrs;
    let gamepad_id: GamepadId;

    // wait for the gamepad to connect
    println!("Waiting for gamepad to connect!");
    loop {
        gilrs = Gilrs::new().unwrap();
        if let Some((_id, gp)) = gilrs.gamepads().next() {
            gamepad_id = gp.id();
            break;
        }
    }
    println!("{} found!", gilrs.gamepad(gamepad_id).name());
    println!("Gamepad found!");
    loop {
        gilrs.next_event();
        let gamepad = gilrs.gamepad(gamepad_id);

        let mut buttons: HashMap<String, bool> = HashMap::new();

        buttons.insert("North".to_string(), gamepad.is_pressed(Button::North));
        buttons.insert("East".to_string(), gamepad.is_pressed(Button::East));
        buttons.insert("South".to_string(), gamepad.is_pressed(Button::South));
        buttons.insert("West".to_string(), gamepad.is_pressed(Button::West));
        buttons.insert("Left Bumper".to_string(), gamepad.is_pressed(Button::LeftTrigger));
        buttons.insert("Right Bumper".to_string(), gamepad.is_pressed(Button::RightTrigger));
        buttons.insert("Left Trigger".to_string(), gamepad.is_pressed(Button::LeftTrigger2));
        buttons.insert("Right Trigger".to_string(), gamepad.is_pressed(Button::RightTrigger2));
        buttons.insert("Left Thumb".to_string(), gamepad.is_pressed(Button::LeftThumb));
        buttons.insert("Right Thumb".to_string(), gamepad.is_pressed(Button::RightThumb));
        buttons.insert("Start".to_string(), gamepad.is_pressed(Button::Start));
        buttons.insert("Select".to_string(), gamepad.is_pressed(Button::Select));


        let left_stick = (gamepad.value(Axis::LeftStickX), gamepad.value(Axis::LeftStickY));
        let right_stick = (gamepad.value(Axis::RightStickX), gamepad.value(Axis::RightStickY));

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
        let dpad = (dpad_x, dpad_y);

        let joystick_values = JoystickValues::new(buttons, left_stick, right_stick, dpad);
        println!("{:?}", joystick_values);

        thread::sleep(Duration::from_millis(1));
    }
}
