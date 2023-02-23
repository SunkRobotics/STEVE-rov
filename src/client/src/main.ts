import { invoke } from "@tauri-apps/api/tauri";

let greetInputEl: HTMLInputElement | null;
let greetMsgEl: HTMLElement | null;

const feed1 = document.querySelector('#feed1') as HTMLCanvasElement;
// const feed2 = document.querySelector('#feed2') as HTMLImageElement;
let ws_feed1 = new WebSocket("ws://192.168.0.102:3000");
ws_feed1.addEventListener('message', (event: MessageEvent) => {
  event.data.text().then((res: string) => {
    var img = new window.Image();
    img.setAttribute("src", "data:image/jpg;base64," + res);

    // let feed_size = feed1.getBoundingClientRect();
    img.addEventListener("load", function () {
        feed1.getContext("2d")!.drawImage(img, 0, 0, img.width, img.height, 0, 0, feed1.width, feed1.height);
    });
  })
})


async function greet() {
  if (greetMsgEl && greetInputEl) {
    // Learn more about Tauri commands at https://tauri.app/v1/guides/features/command
    greetMsgEl.textContent = await invoke("greet", {
      name: greetInputEl.value,
    });
  }
}

window.addEventListener("DOMContentLoaded", () => {
  greetInputEl = document.querySelector("#greet-input");
  greetMsgEl = document.querySelector("#greet-msg");
  document
    .querySelector("#greet-button")
    ?.addEventListener("click", () => greet());
});
