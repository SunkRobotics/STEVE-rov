const feed1 = document.querySelector('#feed1') as HTMLCanvasElement;
// const feed2 = document.querySelector('#feed2') as HTMLImageElement;
let ws_feed1 = new WebSocket("ws://192.168.0.102:3000");

ws_feed1.addEventListener('message', (event: MessageEvent) => {
  event.data.text().then((res: string) => {
    var img = new Image();
    img.setAttribute("src", "data:image/jpg;base64," + res);

    const feed1_ctx = feed1.getContext("2d")!;
    img.addEventListener("load", function () {
        feed1_ctx.drawImage(img, 0, 0, img.width, img.height, 0, 0, 1280, 720);
    });
  })
})
ws_feed1.addEventListener('close', (_) => {
  let img = new Image();
  img.setAttribute("src", "/src/assets/static.gif");
  const feed1_ctx = feed1.getContext("2d")!;
  feed1_ctx.drawImage(img, 0, 0, img.width, img.height, 0, 0, 1280, 720);
})

ws_feed1.addEventListener('error', (_) => {
  let img = new Image();
  img.setAttribute("src", "/src/assets/static.gif");
  const feed1_ctx = feed1.getContext("2d")!;
  feed1_ctx.drawImage(img, 0, 0, img.width, img.height, 0, 0, 1280, 720);
})

let gamepad: Gamepad | null;
window.addEventListener("gamepadconnected", (event) => {
  gamepad = event.gamepad;
});

window.addEventListener("gamepaddisconnected", (_) => {
  gamepad = null;
});
