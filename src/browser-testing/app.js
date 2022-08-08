console.log("App starting...");

var files = ["Jul-26-2022.csv", "Mar-25-2022.csv"];

for (index in files) {
	$("#files").append(new Option((text = files[index]), (value = files[index])));
}

var csv_data;
var x_data;
var y_data;
var z_data;
var surface_data;

graph();

async function graph() {
	console.log("Initializing...");

	csv_data = [];
	x_data = [];
	y_data = [];
	z_data = [];
	surface_data = [];

	console.log("Fetching data...");

	await getData();

	if ($("#contour").is(":checked")) {
		$("#graph-heading").text("Contour Plot");
		contourPlot();
	} else if ($("#surface").is(":checked")) {
		$("#graph-heading").text("Surface Plot");
		surfacePlot();
	} else if ($("#mesh").is(":checked")) {
		$("#graph-heading").text("3D Mesh");
		mesh3d();
	} else if ($("#map").is(":checked")) {
		$("#graph-heading").text("Map Overlay");
		mapOverlay();
	}

	console.log("Done!");
}

async function getData() {
	var url = "../../Data/depth_data/" + $("#files").val();

	await fetch(url, {
		method: "get",
		headers: {
			"content-type": "text/csv;charset=UTF-8",
		},
	})
		.then((response) => {
			// console.log(response.text())
			return response.text();
		})
		.then((data) => {
			csv_data = data.split("\r\n");
		})
		.then(() => {
			for (index in csv_data) {
				csv_data[index] = csv_data[index].split(",");
				if (index > 0) {
					y_data.push(+csv_data[index][0]);
					x_data.push(+csv_data[index][1]);
					z_data.push(+csv_data[index][2]);
				}
			}
		})
		.then(() => {
			console.log(csv_data);
			console.log(x_data);
			console.log(y_data);
			console.log(z_data);

			for (value in z_data) {
				surface_data.push(z_data);
				// var temp = []
				// for (row in z_data){
				//     temp.push(z_data[value])
				// }
				// surface_data.push(temp)
			}
		});
}

function contourPlot() {
	console.log("Creating contour plot...");

	var data = [
		{
			x: x_data,
			y: y_data,
			z: z_data,
			type: "contour",
			// contours: {
			//     coloring: 'heatmap'
			// },
			colorbar: {
				title: "Depth (ft)",
				titleside: "right",
			},
		},
	];

	var layout = {
		autosize: true,
		height: "600",
		margin: {
			l: 70,
			r: 0,
			b: 40,
			t: 30,
		},
	};

	Plotly.newPlot("plot-div", data, layout);
}

function surfacePlot() {
	console.log("Creating surface plot...");

	console.log(surface_data);
	console.log(Math.max(...z_data));

	var data = [
		{
			z: surface_data,
			type: "surface",
			x: x_data,
			y: y_data,
			// z: z_data,
			// type: "mesh3d",
		},
	];

	var layout = {
		autosize: true,
		height: "600",
		margin: {
			l: 0,
			r: 0,
			b: 0,
			t: 30,
		},
		scene: {
			xaxis: {
				title: "Longuitud",
			},
			yaxis: {
				title: "Latitude",
			},
			zaxis: {
				title: "Depth",
				// autorange: "reversed",
				range: [Math.max(...z_data) * 2, 0],
			},
		},
	};

	Plotly.newPlot("plot-div", data, layout);
}

function mesh3d() {
	console.log("Creating 3D mesh...");

	var data = [
		{
			z: z_data,
			x: x_data,
			y: y_data,
			type: "mesh3d",
			opacity: 1.0,
		},
	];

	var layout = {
		autosize: true,
		height: "600",
		margin: {
			l: 0,
			r: 0,
			b: 0,
			t: 30,
		},
		scene: {
			xaxis: {
				title: "Longuitud",
			},
			yaxis: {
				title: "Latitude",
			},
			zaxis: {
				title: "Depth",
				autorange: "reversed",
			},
		},
	};

	Plotly.newPlot("plot-div", data, layout);
}

function mapOverlay() {
	console.log("Creating Map Overlay...");

	var data = [
		{
			type: "densitymapbox",
			lon: x_data,
			lat: y_data,
			z: z_data,
		},
	];

	var layout = {
		mapbox: {
			style: "open-street-map",
		},
		xaxis: {
			title: csv_data[1],
		},
		yaxis: {
			title: csv_data[0],
		},
		height: "900",
		margin: {
			l: 0,
			r: 0,
			b: 0,
			t: 30,
		},
	};

	Plotly.newPlot("plot-div", data, layout);
}
