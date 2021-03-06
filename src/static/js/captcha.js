var year_1, x_1, y_1, year_2, x_2, y_2;

async function startChallenge() {
    await fetchImages();
    document.getElementById("loading").classList.toggle("loader")
    document.getElementById("not_a_robot_checkbox").classList.remove("enable")
    document.getElementById("not_a_robot_checkbox").classList.add("disable")
}

async function nextChallenge() {
    toggleChallenge(1);
    toggleChallenge(2);
}

function clearCheckbox() {
    document.getElementById("building1").checked = false;
    document.getElementById("water1").checked = false;
    document.getElementById("land1").checked = false;
    document.getElementById("church1").checked = false;
    document.getElementById("oiltank1").checked = false;
    document.getElementById("building2").checked = false;
    document.getElementById("water2").checked = false;
    document.getElementById("land2").checked = false;
    document.getElementById("church2").checked = false;
    document.getElementById("oiltank2").checked = false;
}

function verifyCheckbox1() {
    if (document.getElementById("building1").checked === false &&
        document.getElementById("water1").checked === false &&
        document.getElementById("land1").checked === false) {
        return false;
    }
    return true;
}

function verifyCheckbox2() {
    if (document.getElementById("building2").checked === false &&
        document.getElementById("water2").checked === false &&
        document.getElementById("land2").checked === false) {
        return false;
    }
    return true;
}


async function submitChallenge() {
    toggleChallenge(2);

    var building1 = document.getElementById("building1").checked;
    var water1 = document.getElementById("water1").checked;
    var land1 = document.getElementById("land1").checked;
    var church1 = document.getElementById("church1").checked;
    var oiltank1 = document.getElementById("oiltank1").checked;


    var building2 = document.getElementById("building2").checked;
    var water2 = document.getElementById("water2").checked;
    var land2 = document.getElementById("land2").checked;
    var church2 = document.getElementById("church2").checked;
    var oiltank2 = document.getElementById("oiltank2").checked;


    data =
        [{
            'year': year_1,
            'x': x_1,
            'y': y_1,
            'building': building1,
            'water': water1,
            'land': land1,
            'church': church1,
            'oiltank': oiltank1
        },
            {
                'year': year_2,
                'x': x_2,
                'y': y_2,
                'building': building2,
                'water': water2,
                'land': land2,
                'church': church2,
                'oiltank': oiltank2
            }]
    if (verifyCheckbox1() === false || verifyCheckbox2() === false) {
        result.innerHTML = "Please select at least one label";
        document.getElementById("not_a_robot_checkbox").classList.remove("disable");
        document.getElementById("not_a_robot_checkbox").classList.add("enable");
        document.getElementById("loading").classList.toggle("loader");
        clearCheckbox();
        return;
    }
    fetch("/submit_captcha/", {
        method: "POST",
        body: JSON.stringify(data),
        credentials: 'include' //
    }).then(response => {
        var result = document.getElementById("result");
        if (response.status === 200) {
            //result.innerHTML = "Correct";
            clearCheckbox();

            response.text().then(function (text) {
                result.innerHTML = "Correct CAPTCHA. Tile registered."
                document.getElementById("checkmark").classList.add("checkmark_success")
                
                // If the CAPTCHA is embeded this will signal the website that it's completed.
                parent.postMessage(text, "*");
            })
            
        } else {
            response.text().then(function (text) {
                result.innerHTML = text + ". Please try again.";
            })
            clearCheckbox();
        }
    })
    document.getElementById("not_a_robot_checkbox").classList.remove("disable")
    document.getElementById("not_a_robot_checkbox").classList.add("enable")
    document.getElementById("loading").classList.toggle("loader")
}

async function fetchImages() {
    const response = await fetch('/get_tile');
    const json = await response.json();

    console.log(json);

    year_1 = json[0].year;
    x_1 = json[0].x;
    y_1 = json[0].y;

    year_2 = json[1].year;
    x_2 = json[1].x;
    y_2 = json[1].y;

    var image1 = document.getElementById("ch_img1")

    loadImage(image1, "https://tiles.arcgis.com/tiles/nSZVuSZjHpEZZbRo/arcgis/rest/services/Historische_tijdreis_" + year_1 + "/MapServer/tile/11/" + y_1 + "/" + x_1)
        .then(img => {
            // If the image is empty (transparent) load a new one, otherwise load the second one
            var pixelAlpha = getPixel(image1, 1, 1)[3]
            if (pixelAlpha == 0) {
                fetchImages();
            } else {
                var image2 = document.getElementById("ch_img2")
                loadImage(image2, "https://tiles.arcgis.com/tiles/nSZVuSZjHpEZZbRo/arcgis/rest/services/Historische_tijdreis_" + year_2 + "/MapServer/tile/11/" + y_2 + "/" + x_2)
                    .then(img => {
                            // If the image is empty (transparent) load a new one, otherwise show the first one
                            var pixelAlpha = getPixel(image2, 1, 1)[3]
                            if (pixelAlpha == 0) {
                                fetchImages();
                            } else {
                                toggleChallenge(1);
                            }
                        }
                    ).catch(error => fetchImages())
            }
        }).catch(error => fetchImages())
}

function toggleChallenge(id) {
    var popup = document.getElementById("challenge" + id);
    popup.classList.toggle("show");
}

function getPixel(img, x, y) {
    var canvas = document.createElement('canvas');
    var context = canvas.getContext('2d');
    context.drawImage(img, 0, 0);
    return context.getImageData(x, y, 1, 1).data;
}

function loadImage(img, url) {
    return new Promise((resolve, reject) => {
        img.addEventListener('load', e => resolve(img));
        img.addEventListener('error', () => {
            reject(new Error(`Failed to load image's URL: ${url}`));
        });
        img.src = url;
        img.crossOrigin = ''; // Required to get pixel color of the images
    });
}

function show_legend() {
    document.getElementById("legend_info").style.display = "block";
}

function hide_legend() {
    document.getElementById("legend_info").style.display = "none";

}

function checkSize(){
    var height = $('body').outerHeight(); // IMPORTANT: If body's height is set to 100% with CSS this will not work.
    parent.postMessage("resize:" + height, "*");
}

setInterval(checkSize, 500);
