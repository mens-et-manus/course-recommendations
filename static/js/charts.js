var storeCharts = {}

/*

if none: nothing

all:


     radar:
     	assigments
     	expect
     	grading
     	objectives
     	pace
     	rating

if 1:

if more than 1:


*/

function insertEvalStats(id, stats){
	//console.log(stats);
	if(stats.length === 0){
		return;
	}
	// ok, so there is some data
	var ident = "[data-id='" + id + "']";
	$(ident).append("<canvas id=\"chart-"+id+"\" width=\"400\" height=\"400\"></canvas>");
	var chart_ident = "chart-" + id;
	datasets = [];
	for(var i = 0; i < stats.length; i++){
		s = stats[i];
		var data = [
			s.stats.assignments.avg,
			s.stats.expect.avg,
			s.stats.grading.avg,
			s.stats.objectives.avg,
			s.stats.pace.avg,
			s.stats.rating.avg
		];

		datasets.push({
			label: s.season + " " + s.year,
            backgroundColor: "rgba(179,181,198,0.2)",
            borderColor: "rgba(179,181,198,1)",
            pointBackgroundColor: "rgba(179,181,198,1)",
            pointBorderColor: "#fff",
            pointHoverBackgroundColor: "#fff",
            pointHoverBorderColor: "rgba(179,181,198,1)",
            data: data
        });
        console.log(datasets);
	}
	var newChart = new Chart(document.getElementById(chart_ident).getContext("2d"),{
		type: 'radar',
		data: {
			labels: ["Assigments contribute to learning","Subject expectations were met","Grading was fair","Student learning objectives were met","Pace of the class","Rating"],
			datasets: datasets
		},
		options: {
	            scale: {
	                ticks: {
	                    beginAtZero: true
	                }
	            }
	    }
	});
	storeCharts[id] = newChart;
}

function clearCharts(){
	storeCharts = {};
}
