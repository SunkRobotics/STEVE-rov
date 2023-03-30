#[allow(dead_code)]
extern crate serde_json;
use anyhow::Result;
use early_returns::{ok_or_continue, some_or_return};
use gilrs::{Axis, Button, Event, Gamepad, GamepadId, Gilrs, GilrsBuilder};
use serde::Serialize;
use std::collections::HashMap;
use std::thread;
use std::time::Duration;
use tungstenite::Message;
use url::Url;

#[derive(Debug, Serialize)]
struct JoystickValues {
    buttons: HashMap<String, bool>,
    left_stick: (f32, f32),
    right_stick: (f32, f32),
    dpad: (i8, i8),
}

impl JoystickValues {
    pub fn new(gamepad: Gamepad) -> JoystickValues {
        let buttons = JoystickValues::get_buttons(gamepad);
        let left_stick = JoystickValues::get_left_stick(gamepad);
        let right_stick = JoystickValues::get_right_stick(gamepad);
        let dpad = JoystickValues::get_dpad(gamepad);

        JoystickValues {
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

fn main() -> Result<()> {
    let mut gilrs: Gilrs;
    // let mut websocket: Option = None;
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
        // if let None = websocket {
        //     loop {
        //         if let Ok((mut socket, _)) =
        //             // tungstenite::connect(Url::parse("ws://192.168.100.1:8765")?)
        //              tungstenite::connect(Url::parse("ws://localhost:8765")?)
        //         {
        //             println!("Connected!");
        //             let client_info = String::from(r#"{"client_info": "joystick"}"#);
        //             ok_or_continue!(socket.write_message(Message::Text(client_info)));

        //             websocket = Some(socket);
        //             break;
        //         } else {
        //             thread::sleep(Duration::from_millis(1));
        //             continue;
        //         };
        //     }
        // }
        gilrs.next_event();
        let gamepad = gilrs.gamepad(gamepad_id);

        let joystick_values = JoystickValues::new(gamepad);

        println!("{:#?}", joystick_values);
        // if let Some(ws) = websocket.as_mut() {
        //     match ws.write_message(Message::Text(serde_json::to_string(&joystick_values)?)) {
        //         Ok(()) => (),
        //         Err(error) => {
        //             websocket = None;
        //             eprintln!("Websocket Error!");
        //             eprintln!("{error}");
        //         }
        //     }
        // }
        thread::sleep(Duration::from_millis(1));
    }
}
