console.log("App starting...")

var files = [
    "Jul-26-2022.csv",
    "Mar-25-2022.csv"
]

for (index in files) {
    $("#files").append(new Option(
        text = files[index],
        value = files[index]
    ))
}

var csv_data;
var x_data;
var y_data;
var z_data;

async function graph() {

    console.log("Initializing...")

    csv_data = [];
    x_data = [];
    y_data = [];
    z_data = [];

    console.log("Fetching data...")

    await getData()

    if ($("#plot").is(":checked")){
        await plot()
    }

    else if ($("#surface").is(":checked")){
        await surfacePlot()
    }

    else if ($("#map").is(":checked")){
        await mapOverlay()
    }
    
    console.log("Done!")

}

async function getData() {

    var url = "../../Data/depth_data/" + $("#files").val();

    await fetch(url, {
        method: 'get',
        headers: {
            'content-type': 'text/csv;charset=UTF-8',
        }
    })
        .then(response => {
            // console.log(response.text())
            return response.text()
        })
        .then(data => {
            csv_data = data.split("\r\n")
        })
        .then(() => {
            for (index in csv_data) {
                csv_data[index] = csv_data[index].split(",");
                if (index > 0) {
                    z_data.push(csv_data[index])
                    x_data.push(csv_data[index][0])
                    y_data.push(csv_data[index][1])
                }
            }
        })
        .then(() => {
            console.log(csv_data)
            console.log(x_data)
            console.log(y_data)
            console.log(z_data)
        })
}

function plot() {
    console.log("Creating 2D Plot...")

    // Define Data
var data = [{
    z: z_data,
    type:"surface"
  }];
  
  // Define Layout
  var layout = {
    xaxis: {
        title: csv_data[0][0]
    },
    yaxis: {
        title: csv_data[0][1]
    },
    title: "Bathymetry Map - Parguera"
  };

  Plotly.newPlot("plot-div", data, layout)

}

function surfacePlot() {
    console.log("Creating 3D Surface Plot...")

    data = [{
        title: "Surface Plot",
        z: z_data,
    }]

    layout = {

    }

    config = {

    }

    Plotly.newPlot("plot-div", data, layout, config)
}

function mapOverlay() {
    console.log("Creating Map Overlay...")
}
