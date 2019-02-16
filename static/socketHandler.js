function getAge(birthDate){
	var born = new Date(birthDate)
	var ageDifMs = Date.now() - born.getTime();
    var ageDate = new Date(ageDifMs); // miliseconds from epoch
    return Math.abs(ageDate.getUTCFullYear() - 1970);
}

function result(name, photo, bio, birthDate){

	var age = getAge(birthDate)


	return '<div class="card">\
				<div class="card-body row">\
					<div class="col-md-3">\
						<img src="'+photo+'" height="150px" width="150px"/>\
					</div>\
					<div class="col-md-9" id="results-container">\
						<h3>'+name+' | '+age+'</h3>\
						<p>'+bio+'</p>\
					</div>\
				</div>\
			</div>'
}


// Socket event listeners for handling data recieved from the server
socket.on('connect', function() {
    console.log("Server connected")
});

//When logged stringify and save profile to local storage
//Then navigate to launch screen
socket.on('logged_in', function(profile) {
	window.localStorage.setItem("profile", JSON.stringify(profile));
    render(flow.launch(profile))
});

//When recommendations are received from the server
socket.on('recs', function(recs){
	for (var i = 0; i < recs.length; i++) {
		console.log(recs[i])
		name = recs[i].name
		photo = recs[i].photos[0].url
		bio = recs[i].bio
		birthDate = recs[i].birth_date
		cardResult = result(name, photo, bio, birthDate)
		$('#results-container').append(cardResult)
	}
})

socket.on('phone_auth_success', function(){
	$('#phoneAuthCodeSection').attr('class', 'shown');
})

socket.on('phone_auth_failure', function(){
	console.log('phone_auth_failure')
})