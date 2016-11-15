$(document).ready(function(){
	//$("#part-1").css("width",$(window).width() + "px");
	$("#part-1").css("height",$(window).height() + "px");
	$("#part-1 svg").attr("height",$(window).height());
	$("#part-1 svg").attr("width",$(window).width());
	$("#part-1 svg").attr("viewbox", "0 0 " + $(window).width() + " " + $(window).height());

	
	var w = $(window).width() / 20;
	var num_w = 20;
	var h = $(window).height() / 20;
	var num_h = 20;
	for(var i = 0; i < num_w; i++){
		var svgns = "http://www.w3.org/2000/svg";
		var group = document.createElementNS(svgns, "g");
		group.setAttribute('id', 'group-' + (i+1));
		for(var j = 0; j < num_h; j++){
			var svgns = "http://www.w3.org/2000/svg";
			var ret = 	document.createElementNS(svgns, "rect");
			ret.setAttributeNS(null,'x',i*w);
			ret.setAttributeNS(null,'y',j*h);
			ret.setAttributeNS(null,'height',h);
			ret.setAttributeNS(null,'width',w);
			ret.setAttributeNS(null,'fill','#F44336');
			ret.setAttributeNS(null,'stroke-width',1);
			ret.setAttributeNS(null,'stroke','#F44336');
			group.appendChild(ret);
		}
		document.querySelector("#part-1 svg").appendChild(group);
	}
	window.setTimeout(function(){
		$("#part-1 svg rect").velocity("transition.slideDownIn",{
			stagger: 10
		});
	},100);

	window.setInterval(function(){
		//switch some random tiles to different colors
		var array = $("#part-1 svg rect").toArray();
		var randomIndex = getRandomInt(0,array.length-1);
		var randomRect = array[randomIndex];
		$(randomRect).velocity({
			fill: "#eee",
			stroke: "#eee"
		},{
			duration: 1000,
			complete: function(){
				$(this).velocity({
					fill: "#F44336",
					stroke: "#F44336"
				});
			}
		});
	}, 100);

	/*
	+-------------------------------------------+
	|
	|
	|
	|
	|     __*____
	|   _/       \
	|  /          \
	| /            \
	|/              __* ...........
	*
	|
	+--------------------------------------------+
	*/


	$.getJSON("/stats", function(data){
		for(key in data){
			var _d = data[key];
			if(typeof _d === "number"){
				_d = Math.round(_d);
			}
			var id = "#stats-" + key;
			if(key.split("_").reverse()[0] === "rating" && typeof _d === "number"){
				$(id).html(generateStars(_d));
			}
			else{
				$(id).text(_d);
			}
		}
	});
});

function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function generateStars(rating){
	var to_push = "<span>"
	for(var i = 0; i < rating; i++){
		to_push = to_push + "<i class='fa fa-star star-selected'></i>";
	}
	for(var i = 0; i < (5-rating); i++){
		to_push = to_push + "<i class='fa fa-star'></i>";
	}
	to_push = to_push + "</span>";
	return to_push;
}