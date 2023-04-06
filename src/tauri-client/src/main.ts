const feed1 = document.querySelector('#feed1') as HTMLCanvasElement;
// let ws_feed1 = new WebSocket("ws://192.168.100.2:3000");
let ws_feed1 = new WebSocket("ws://localhost:3000");
let feed1_ctx = feed1.getContext("2d")!;
ws_feed1.binaryType = "arraybuffer";

// ws_feed1.addEventListener('message', (event: MessageEvent) => {
//   event.data.text().then((res: string) => {
//     var img = new Image();
//     img.img = new Buffer.from()

//     const feed1_ctx = feed1.getContext("2d")!;
//     img.addEventListener("load", function () {
//         // feed1_ctx.drawImage(img, 0, 0, img.width, img.height, 0, 0, feed1.width, feed1.height);
//         // feed1_ctx.drawImage(img, 0, 0, img.width, img.height);
//         //  feed1_ctx.drawImage(img, 0, 0);
//     });
//   })
// })
ws_feed1.addEventListener('message', (event: MessageEvent) => {
  var frame = new Image();
  frame.src = "data:image/jpg;base64," + btoa(
    new Uint8Array(event.data).reduce(
        (data, byte) => data + String.fromCharCode(byte), '')
  );

  // const feed1_ctx = feed1.getContext("2d")!;
  // feed1_ctx.drawImage(frame, 0, 0);
  frame.addEventListener("load", function () {
    feed1_ctx.drawImage(frame, 0, 0);
  });
})

ws_feed1.addEventListener('close', (_) => {
  let img = new Image();
  img.setAttribute("src", "src/assets/static.gif");
  const feed1_ctx = feed1.getContext("2d")!;
  feed1_ctx.drawImage(img, 0, 0, img.width, img.height, 0, 0, 1280, 720);
})

ws_feed1.addEventListener('error', (_) => {
  let img = new Image();
  img.setAttribute("src", "src/assets/static.gif");
  const feed1_ctx = feed1.getContext("2d")!;
  feed1_ctx.drawImage(img, 0, 0, img.width, img.height, 0, 0, 1280, 720);
})


const feed2 = document.querySelector('#feed2') as HTMLCanvasElement;
let ws_feed2 = new WebSocket("ws://192.168.100.7:3000");


/*
ws_feed2.addEventListener('message', (event: MessageEvent) => {
  event.data.text().then((res: string) => {
    var img = new Image();
    img.setAttribute("src", "data:image/jpg;base64," + res);

    const feed2_ctx = feed2.getContext("2d")!;
    img.addEventListener("load", function () {
        let decoder = new ImageDecoder({
          type: "image/jpeg",
          data: event.data
        });

        let frame = decoder.decode().then((res) => {
          feed2_ctx.drawImage(res.image, 0, 0);
        })// feed1_ctx.drawImage(img, 0, 0, img.width, img.height, 0, 0, feed1.width, feed1.height);
        // feed1_ctx.drawImage(img, 0, 0, img.width, img.height);
        //  feed1_ctx.drawImage(img, 0, 0);
    });
  })
})
ws_feed2.addEventListener('close', (_) => {
  let img = new Image();
  img.setAttribute("src", "/src/assets/static.gif");
  const feed2_ctx = feed2.getContext("2d")!;
  feed2_ctx.drawImage(img, 0, 0, img.width, img.height, 0, 0, 1280, 720);
})

ws_feed2.addEventListener('error', (_) => {
  let img = new Image();
  img.setAttribute("src", "/src/assets/static.gif");
  const feed2_ctx = feed2.getContext("2d")!;
  feed2_ctx.drawImage(img, 0, 0, img.width, img.height, 0, 0, 1280, 720);
})
*/
