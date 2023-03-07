use gilrs::Gilrs;

fn main() {
    let mut gilrs = Gilrs::new().unwrap();
    for (_id, gamepad) in gilrs.gamepads() {
        println!("{} is {:?}", gamepad.name(), gamepad.power_info());
    }
    let mut active_gamepad = None;
    loop {
        while let Some(event) = gilrs.next_event() {
            active_gamepad = Some(event.id);
        }
        if let Some(gamepad) = active_gamepad.map(|id| gilrs.gamepad(id)) {
            let gamepad_state = gamepad.state();
            let mut buttons_values: Vec<bool> = Vec::new();
            for (_, button) in gamepad_state.buttons() {
                buttons_values.push(button.is_pressed());
            }
            println!("{:?}", buttons_values);
        }
    }
}
