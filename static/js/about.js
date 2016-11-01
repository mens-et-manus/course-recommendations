$(document).ready(function(){
	$("#part-1").css("width",$(window).width() + "px");
	$("#part-1").css("height",$(window).height() + "px");
	$("#part-1 svg").attr("height",$(window).height());
	$("#part-1 svg").attr("width",$(window).width());
	$("#part-1 svg").attr("viewbox", "0 0 " + $(window).width() + " " + $(window).height());

	/*
	var w = $(window).width() / 20;
	var num_w = 20;
	var h = $(window).height() / 20;
	var num_h = 20;
	for(var i = 0; i < num_w; i++){
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
			document.querySelector("#part-1 svg").appendChild(ret);
		}
	}
	window.setTimeout(function(){
		$("#part-1 svg > rect").velocity("transition.slideDownIn",{
			stagger: 10
		});
	},100);

	window.setInterval(function(){
		//switch some random tiles to different colors
	}, 400);
	*/

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
});