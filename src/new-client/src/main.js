let cam1 = document.getElementById("cam1");
let cam2 = document.getElementById("cam2");

let metric = 1;
let pixPerMetric = 0;
let points = []

function takePicture() {
    let new_space = document.createElement("div")

    new_space.className = "newSpace"

    let info = document.createElement("p")
    let pic = document.createElement("img")

    pic.src = "countries.jpg"

    pic.addEventListener("click", (e) => {
        points.push([e.offsetX, e.offsetY])

        if (points.length == 2) {
            let difX = points[0][0] - points[1][0]
            let difY = points[0][1] - points[1][1]

            let distance = Math.sqrt(difX**difX + difY**difY)
            console.log(distance)

            pixPerMetric = distance / metric
        }

        if (points.length == 4) {
            let difX = points[2][0] - points[3][0]
            let difY = points[2][1] - points[3][1]

            let pixDistance = Math.sqrt(difX**difX + difY**difY)

            let distance = pixDistance / pixPerMetric

            new_space.querySelector("p").innerHTML = `${distance}`

            points = []
        }
    })

    new_space.appendChild(pic)
    new_space.appendChild(info)

    document.body.appendChild(new_space);
}

