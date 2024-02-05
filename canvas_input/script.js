let canvas = document.getElementById('canvas');
let ctx = canvas.getContext('2d');
let rect = {};
let drag = false;
let rectangles = []; // Array to store rectangles

function init() {
    canvas.addEventListener('mousedown', mouseDown, false);
    canvas.addEventListener('mouseup', mouseUp, false);
    canvas.addEventListener('mousemove', mouseMove, false);
}

function mouseDown(e) {
    const colorInput = document.getElementById("colorvalue").value;
    const labelInput = document.getElementById('labelInput').value;

    // Check if the color or label inputs are empty
    if (!colorInput || !labelInput) {
        alert('Please enter both a color and a label before drawing.');
        return; // Exit the function if either input is empty
    }

    // Proceed with setting up the rectangle if both inputs are provided
    rect = { 
        startX: e.pageX - canvas.offsetLeft, 
        startY: e.pageY - canvas.offsetTop, 
        w: 0, 
        h: 0, 
        color: colorInput, 
        label: labelInput
    };
    drag = true;
}


function mouseUp() {
    drag = false;
    rectangles.push(rect); // Add the rectangle to the array
    color = document.getElementById("colorvalue").value
    drawAll()
}

function mouseMove(e) {
    if (drag) {
        rect.w = (e.pageX - canvas.offsetLeft) - rect.startX;
        rect.h = (e.pageY - canvas.offsetTop) - rect.startY;
        drawAll(); // Redraw all rectangles
    }
}

function drawAll() {
    ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear the canvas
    rectangles.forEach(function(r) { // Loop through all rectangles and draw them
        ctx.strokeStyle = r.color;
        ctx.strokeRect(r.startX, r.startY, r.w, r.h);
    });
}

function saveJsonToFile(jsonData, filename) {
    const jsonString = JSON.stringify(jsonData, null, 4); // null and 4 are used for formatting

    // Create a Blob object with the JSON string
    const blob = new Blob([jsonString], { type: 'application/json' });

    // Create an object URL for the Blob
    const url = URL.createObjectURL(blob);

    // Create a new <a> element
    const link = document.createElement('a');

    // Set the download attribute of the <a> element with the desired filename
    link.download = filename;

    // Set the href of the link to the object URL
    link.href = url;

    // Append the <a> element to the body
    document.body.appendChild(link);

    // Programmatically click the <a> element to trigger the download
    link.click();

    // Remove the <a> element from the body
    document.body.removeChild(link);

    // Release the object URL
    URL.revokeObjectURL(url);
}

function saveRectangle() {

    const bkgInput = document.getElementById("background").value;
    const negInput = document.getElementById("negative").value;

    if (!bkgInput) {
        alert('Please enter both a color and a label before drawing.');
        return; // Exit the function if either input is empty
    }

    let allRectData = []
    for (rect of rectangles){
        let rectData = {
            label: rect.label,
            startX: rect.startX,
            startY: rect.startY,
            endX: rect.startX + rect.w,
            endY: rect.startY + rect.h,
            color: rect.color
        };
        allRectData.push(rectData)
    }
    
    let outputData = {}
    outputData['rectangles'] = allRectData
    outputData['background'] = bkgInput
    outputData['negative'] = negInput

    // console.log(JSON.stringify(allRectData));
    saveJsonToFile(outputData, "data.json");

    // Send rectangleData to the server
    fetch('/raw_canvas_implementation_1/save_rectangle.php', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(allRectData),
    })
    .then(response => {
        // Debugging: Log the raw response
        console.log('Raw response:', response);
    
        // Clone the response stream in order to log it and then parse it as JSON
        const clonedResponse = response.clone();
    
        // Debugging: Log the response text
        clonedResponse.text().then(text => console.log('Response text:', text));
        
        // Check if the response is OK and is of type JSON before parsing
        if (response.ok && response.headers.get("Content-Type")?.includes("application/json")) {
            return response.json();
        } else {
            throw new Error('Response was not JSON');
        }
    })
    .then(data => {
        console.log('Parsed JSON:', data);
        // Handle your JSON data here
    })
    .catch((error) => {
        console.error('Error:', error);
    });
    
   document.getElementById('labelInput').value = '';
}

document.getElementById('saveBtn').addEventListener('click', saveRectangle);

init();
