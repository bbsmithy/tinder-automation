function getAge(birthDate){
	var born = new Date(birthDate)
	var ageDifMs = Date.now() - born.getTime();
    var ageDate = new Date(ageDifMs); // miliseconds from epoch
    return Math.abs(ageDate.getUTCFullYear() - 1970);
}

function createResultCard(result){

	var age = getAge(result.birthDate)


	return '<div class="card" id="'+result.id+'">\
				<div class="card-body row">\
					<div class="col-md-3">\
						<img src="'+result.photo+'" height="150px" width="150px"/>\
					</div>\
					<div class="col-md-6" id="results-container">\
						<h3>'+result.name+' | '+age+'</h3>\
						<p>'+result.bio+'</p>\
					</div>\
					<div class="col-md-3" class="likeAndDislikeDisplay">\
						\
					</div>\
				</div>\
			</div>'
}

function renderRecs(recs){
	for (var i = 0; i < recs.length; i++) {	
		cardResult = createResultCard({
			name: recs[i].name,
			photo: recs[i].photos[0].url,
			bio: recs[i].bio,
			birthDate: recs[i].birth_date,
			id: recs[i]._id
		})
		$('#results-container').append(cardResult)
	}
}


// Socket event listeners for handling data recieved from the server
socket.on('connect', function() {
    console.log("Server connected")
});

socket.on('disconnect', function() {
    console.log("Server disconnected")
});

//When logged stringify and save profile to local storage
//Then navigate to launch screen
socket.on('logged_in', function(profile, initialRecs) {
	window.sessionStorage.setItem("profile", JSON.stringify(profile));
    render(flow.launch(profile))
    renderRecs(initialRecs)
});

socket.on('phone_auth_success', function(){
	$('#phoneAuthCodeSection').attr('class', 'shown');
})

socket.on('phone_auth_failure', function(){
	console.log('phone_auth_failure')
})

//When recommendations are received from the server
socket.on('recs', function(recs){
	renderRecs(recs)
})


socket.on('like', function(id){
	var result = document.getElementById(id)
	result.parentNode.removeChild(result);
})