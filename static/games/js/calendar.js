
function radioSelect(id){
	if (id=="tba") {
		document.getElementById("input_year").className="display-none"
		document.getElementById("input_release").className="display-none"
	} else if (id=="year") {
		document.getElementById("input_year").className="display-block"
		document.getElementById("input_release").className="display-none"
	} else {
		document.getElementById("input_year").className="display-none"
		document.getElementById("input_release").className="display-block"
	}
};

function clearModal(){
	emptylist();
	var success=document.getElementById("js-game-added-success");
	if(success!=null){
		success.className="display-none";
	}
	var fail=document.getElementById("js-game-added-failure");
	if(fail!=null){
		fail.className="display-none";
	}
	var newgame=document.getElementById("js-add-new-game-form");
	if(newgame!=null){
		newgame.reset();
	}
	 
	document.getElementById("js-search-games-form").reset();
	document.getElementById("js-cant-find").className="text-center mt-4 display-block";
	document.getElementById("js-add-game").className="display-none";
}

function showAddGames(){
	document.getElementById("js-cant-find").className="display-none";
	document.getElementById("js-add-game").className="month mt-3 display-block";
};

function emptylist(){
	document.getElementById("js-clear-list").className="display-none";
	gameList=document.getElementById("js-games-to-add");
	while (gameList.firstChild) {
		gameList.removeChild(gameList.firstChild);
	};
};

function addGameToProfile(gameId){
	xhttpAdd = new XMLHttpRequest();
	xhttpAdd.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			var addedgame = JSON.parse(xhttpAdd.responseText);
			var gameAddButton=document.getElementById("gameAddButton"+gameId)
			gameAddButton.className="btn grey-background black-text m-2 p-2";
			gameAddButton.innerHTML=addedgame["status"];
			gameAddButton.disabled=true;
		}
	};
	var urlAddGame="/addGameToProfile?id="+gameId
	xhttpAdd.open("GET",urlAddGame,true)
	xhttpAdd.send() 
}

function removeGameFromProfile(gameId){
	xhttpRemove = new XMLHttpRequest();
	xhttpRemove.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			var removedgame = JSON.parse(xhttpRemove.responseText);
			var gameRemoveButton=document.getElementById("gameRemoveButton"+gameId)
			gameRemoveButton.className="btn grey-background black-text m-2 p-2";
			gameRemoveButton.innerHTML=removedgame["status"];
			gameRemoveButton.disabled=true;
		}
	};
	var urlAddGame="/removeGameFromProfile?id="+gameId
	xhttpRemove.open("GET",urlAddGame,true)
	xhttpRemove.send()
}

function search(){
	emptylist()
	var q=document.getElementById("js-search-query").value;
	document.getElementById("js-clear-list").className="btn nintendo-red-background"
	xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			var games = JSON.parse(xhttp.responseText);
			games.forEach(function(g) {
				var gameLi=document.createElement("li");
				var gameText=document.createTextNode(g["name"])
				gameLi.appendChild(gameText);
				if(g["added"]==0){
					var gameAddButton=document.createElement("button");
					gameAddButton.setAttribute("id","gameAddButton"+g["id"])
					gameAddButton.innerHTML="Add game";
					gameAddButton.className="btn nintendo-red-background m-2 p-2";
					gameAddButton.setAttribute("onclick", "addGameToProfile("+g["id"]+")");
					gameLi.appendChild(gameAddButton)
				}else{
					var gameRemoveButton=document.createElement("button");
					gameRemoveButton.setAttribute("id","gameRemoveButton"+g["id"])
					gameRemoveButton.innerHTML="Remove game";
					gameRemoveButton.className="btn btn-warning m-2 p-2";
					gameRemoveButton.setAttribute("onclick", "removeGameFromProfile("+g["id"]+")");
					gameLi.appendChild(gameRemoveButton)
				}
				document.getElementById("js-games-to-add").appendChild(gameLi);

			});
			
		}
	};
	var urlGetGames="/searchGames?q="+q
	xhttp.open("GET",urlGetGames,true)
	xhttp.send()

};

function addNewGame(){
	document.getElementById("js-game-added-success").className="display-none"
	document.getElementById("js-game-added-failure").className="display-none"
	xhttpAddNewGame = new XMLHttpRequest();
	xhttpAddNewGame.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			var response = JSON.parse(xhttpAddNewGame.responseText);
			if(response["status"]=="success"){
				document.getElementById("js-game-added-success").className="alert alert-success mt-3 mx-auto alert-new-game text-center display-block"
			}else if(response["status"]=="failure") {
				document.getElementById("js-game-added-failure").className="alert alert-danger mt-3 mx-auto alert-new-game text-center display-block"
			}
		}
	};
	var name=document.getElementById("game_name").value
	var type=document.getElementById("game_type").value
	var year=document.getElementById("input_year").value
	var release=document.getElementById("input_release").value
	var radios = document.getElementsByName("radio_date");
	for (var i = 0, length = radios.length; i < length; i++){
		if (radios[i].checked){
	  		radios=radios[i].value
	  		break;
		}
	}
	var csrf=document.getElementsByName("csrfmiddlewaretoken")[0].value
	console.log(csrf)
	var urlAddNewGame="/addNewGame"
	xhttpAddNewGame.open("POST",urlAddNewGame,true)
	var formData = new FormData();
	xhttpAddNewGame.setRequestHeader("X-CSRFToken",csrf);
	formData.append("game_name",name)
	formData.append("game_type",type)
	formData.append("radio_date",radios)
	formData.append("game_year",year)
	formData.append("game_release",release)
	xhttpAddNewGame.send(formData) 
};


