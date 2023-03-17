extern crate anyhow;
extern crate serde_json;
mod gamepad;
use anyhow::Result;
use early_returns::ok_or_continue;
use gamepad::GamepadData;
use gilrs::{GamepadId, Gilrs};
use std::thread;
use std::time::Duration;
use tungstenite::Message;
use url::Url;

pub fn run() -> Result<()> {
    let mut gilrs: Gilrs;
    let mut websocket = None;
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
        if let None = websocket {
            loop {
                if let Ok((mut socket, _)) =
                    // tungstenite::connect(Url::parse("ws://192.168.100.1:8765")?)
                    tungstenite::connect(Url::parse("ws://localhost:8765")?)
                {
                    println!("Connected!");
                    let client_info = String::from(r#"{"client_type": "joystick"}"#);
                    ok_or_continue!(socket.write_message(Message::Text(client_info)));

                    websocket = Some(socket);
                    break;
                } else {
                    thread::sleep(Duration::from_millis(1));
                    continue;
                };
            }
        }
        gilrs.next_event();
        let gamepad = gilrs.gamepad(gamepad_id);

        let joystick_values = GamepadData::new(gamepad);

        if let Some(ws) = websocket.as_mut() {
            match ws.write_message(Message::Text(serde_json::to_string(&joystick_values)?)) {
                Ok(()) => (),
                Err(error) => {
                    websocket = None;
                    eprintln!("Websocket Error!");
                    eprintln!("{error}");
                }
            }
        }
        thread::sleep(Duration::from_millis(1));
    }
}
