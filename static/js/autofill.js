var autoFillInput = function(elem,data,onSelect){
	$(elem).addClass("autofill");
	var html = "<span><i class='fa fa-search'></i></span>"+"<input type='text' placeholder='Search for classes...'><div class='autofill-possible shadow'></div>"+"<span class='autofill-clear'><i class='fa fa-close'></i></span>";
	$(elem).html(html);
	var newElem = $(elem).find("input")
	var sugg = $(elem).find(".autofill-possible")
	this.root = elem
	this.elem = newElem;
	this.possible = sugg;
	this.onSelect = onSelect;

	var newData = [];
	for(var i = 0; i < data.length; i++){
		newData.push({
			id: data[i].id,
			title: data[i].title,
			text: data[i].id + "-" + data[i].title
		});
	}
	this.data = newData;
	var $this = this;
	$(this.root).find(".autofill-clear").click(function(){
		$this.clear();
	});
	$(this.elem).on("change paste keyup",function(){
		var val = $($this.elem).val();
		var matches = []
		$($this.possible).html("")
		if(val.trim() !== ""){
			for(var i = 0; i < $this.data.length; i++){
				if($this.data[i].text.toLowerCase().indexOf(val.toLowerCase()) !== -1){
					matches.push($this.data[i]);
				}
			}
			if(matches.length > 5){ // only get the first 5
				matches = matches.slice(0,5);
			}
			for(var i = 0; i < matches.length; i++){
				$($this.possible).append("<p data-id='"+matches[i].id+"'>" + matches[i].text + "</p>");
			}
		}
		$($this.possible).find("p").each(function(i){
			$(this).click(function(){
				$this.onSelect($(this).attr("data-id"),$(this).text());
			});
		});
	});
}

autoFillInput.prototype.clear = function(){
	$(this.root).find("input").val("")
	$(this.root).find(".autofill-possible").html("")
}