function sendPredictAll(courses, ratings, callback){
	var id = guid()
	var courseList = []
	for(var i = 0; i < ratings.length; i++){
		courseList.push([courses[i],ratings[i]])
	}
	$.ajax({
		method: "POST",
		url: "/predict/all",
		contentType: "application/json",
		data: JSON.stringify({id: id, courseList: courseList, courses: courses, ratings: ratings}),
		dataType: "json"
	})
	.done(function(data){
		callback(data)
	});
}

/*

content -> some rating .rel
collab -> predicted rating .rating

==============
most similar:
* 1
* 2
* 3
=============
similar students liked:
* 1
* 2
* 3

*/

var ai;
var selected_courses = [];
var allCourses = [];
$(document).ready(function(){
	$.get("/storage/classes.json", function(data){
		if(typeof data === typeof ""){	
			data = JSON.parse(data)
		}
		data = data.courses;
		allCourses = data;
		ai = new autoFillInput($("#select-autofill"),data,function(id,text){
			ai.clear();
			if(!alreadyInSelected(id)){
				var to_push = "<div class='row courses' data-id='"+id+"'><p>" + text + "</p><span>";
				for(var i = 0; i < 5; i++){
					if(i === 0){
						to_push = to_push + "<i class='fa fa-star star-selected'></i>";
					}
					else{
						to_push = to_push + "<i class='fa fa-star'></i>";
					}
				}
				to_push = to_push + "</span><span class='course-close'><i class='fa fa-close'></i></span></div>"
				$("#selected-courses").append(to_push);
				$("#selected-courses > div").last().find(".fa-star").each(function(i){
					$(this).click(function(){
						setRating(id, i+1)
					});
				});
				$("#selected-courses > div").last().find(".course-close").click(function(){
					var newArray = [];
					for(var j = 0; j < selected_courses.length; j++){
						if(selected_courses[j].id !== id){
							newArray.push(selected_courses[j])
						}
					}
					selected_courses = newArray;
					$("#selected-courses .courses[data-id='" + id + "']").remove();
				});
				//
				selected_courses.push({
					id: id,
					rating: 1
				});
			}
		});
	});
});

function alreadyInSelected(id){
	for(var i = 0; i < selected_courses.length; i++){
		if(selected_courses[i].id === id){
			return true;
		}
	}
	return false;
}

function setRating(id,rating){
	for(var i = 0; i < selected_courses.length; i++){
		if(selected_courses[i].id === id){
			selected_courses[i].rating = rating;
		}
	}
	var arr = $("#selected-courses .courses[data-id='" + id + "'] .fa-star");
	arr.removeClass("star-selected");
	for(var i = 0; i < rating; i++){
		$(arr.get(i)).addClass("star-selected");
	}
}

function insertCourseItem(containerId, ret, title, contentBased){
	var text = "<span class='courses-courseid'>"+ ret.id + "</span><span class='courses-coursetitle'>" + title + "</span>";
	var to_push = "<div class='row courses courses-rec' data-id='"+ret.id+"'><p>" + text + "</p>"
	//if content-based
	if(contentBased === true){
		to_push = to_push + "<span><a href='http://catalog.mit.edu/subjects/" + ret.id.split(".")[0];
		to_push = to_push + "' target='_blank'><i class='fa fa-link'></i></a><i class='fa fa-eye' style='margin-left: 10px'></i></span>"
		to_push = to_push + "<div class='courses-rec-desc' style='display:none'><p>" + (ret.similarity*100).toFixed(1) + "% similarity to " + ret.originalCourse + "</p></div>";
	}
	else{
		//add the rating stars and stuff
		//ret.rating
		to_push = to_push + "<span>"
		for(var i = 0; i < ret.rating; i++){
			to_push = to_push + "<i class='fa fa-star star-selected'></i>";
		}
		for(var i = 0; i < (5-ret.rating); i++){
			to_push = to_push + "<i class='fa fa-star'></i>";
		}
		to_push = to_push + "</span>"
	}
	//
	to_push = to_push + "</div>"
	$(containerId).append(to_push);
	if(contentBased === true){
		var id = ret.id;
		$(containerId + " > div").last().find(".fa-eye").click(function(i){
			$(this).parent().parent().find(".courses-rec-desc").slideToggle();
		});
	}
}

function predictContent(){
	var ratings = [];
	var courses = [];
	for(var i = 0; i < selected_courses.length; i++){
		ratings.push(selected_courses[i].rating);
		courses.push(selected_courses[i].id);
	}
	sendPredictAll(courses, ratings, function(data){
		//
		//
		// CONTENT-BASED
		//
		//

		var ret = normalizeContentData(data.content);
		var ret2 = normalizeCollabData(data.collab.data);
	    //display the results...
	    $("#predicted-courses-content").html("");
	    $("#predicted-courses-collab").html("");
	    if(ret.length === 0){
	    	//nothing here...
	    }
	    else{
	    	$("#predicted-container").css("display","flex");
	    	for(var i = 0; i < ret.length; i++){
	    		var text = "Error: course not found"
	    		for(var j = 0; j < allCourses.length; j++){
	    			if(allCourses[j].id === ret[i].id){
	    				insertCourseItem("#predicted-courses-content",ret[i],allCourses[j].title,true);
	    			}
	    		}
	    	}
	    	for(var i = 0; i < ret2.length; i++){
	    		var text = "Error: course not found"
	    		for(var j = 0; j < allCourses.length; j++){
	    			if(allCourses[j].id === ret2[i].id){
	    				insertCourseItem("#predicted-courses-collab",ret2[i],allCourses[j].title,false);
	    			}
	    		}
	    	}
	    }


	});
}

function normalizeCollabData(data){
	var ret = [];
	for(key in data){
		if(data[key] !== 0){
			ret.push({
				id: key,
				rating: data[key]
			})	
		}
	}
	ret.sort(function(a,b) {
		return b.rating - a.rating
	});
	if(ret.length > 3){
		ret = ret.slice(0,3)
	}
	return ret;
}

function normalizeContentData(data){
	var ret = [];
	for(var i = 0; i < data.data.length; i++){
		var _d = normalizeDataSet(data.data[i]);
		var _r = data.ratings[i] -1;

		for(var j = 0; j < _d.length; j++){
			var indexExists = -1;
			for(var k = 0; k < ret.length; k++){
				if(ret[k].id === _d[j].id){
					indexExists = k;
				}
			}

			if(indexExists == -1){
				ret.push({
					id: _d[j].id,
					rel: _r * _d[j].num,
					similarity: _d[j].similarity,
					originalCourse: data.courses[i]
				});
			}
			else{
				ret[indexExists].rel = ret[indexExists].rel + (_r * _d[j].num)
			}


		} 
	}

	ret.sort(function(a, b) {
        return b.rel - a.rel //descending order
    });
    if(ret.length > 3){
    	ret = ret.slice(0,3);
    }
    return ret;
}

function normalizeDataSet(data){
	var maxIndex = -1;
	for(var i = 0; i < data.length; i++){
		if(maxIndex === -1 || data[i].num > data[maxIndex].num){
			maxIndex = i;
		}
	}
	if(maxIndex === -1){
		return [];
	}
	var ratio = 5/data[maxIndex].num;
	for(var i = 0; i < data.length; i++){
		data[i].similarity = data[i].num;
		data[i].num = Math.round(ratio * data[i].num);
	}
	return data;
}

function guid() {
  function s4() {
    return Math.floor((1 + Math.random()) * 0x10000)
      .toString(16)
      .substring(1);
  }
  return s4() + s4() + '-' + s4() + '-' + s4() + '-' +
    s4() + '-' + s4() + s4() + s4();
}