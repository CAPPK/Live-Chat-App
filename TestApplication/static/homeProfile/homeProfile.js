function startWeather() {
	var element = document.getElementById('zipcode').value;
	console.log(element);
	makeRec('GET', '/weather?zip=' + element, handleWeather);
}

function handleWeather(response) {
	var object = JSON.parse(response.responseText);
	console.log(object);
	var weather = JSON.parse(object);
	console.log(weather);

	var mainInfo = document.getElementById('mainCont');
	var cityCont = document.createElement('div');
	var city = weather['name'];
	cityCont.innerText = 'City: ' + city;

	var tempCont = document.createElement('div');
	var temp = weather['main']['temp'];
	tempCont.innerText = 'Temp: ' + temp;

	var descCont = document.createElement('div');
	var desc = weather['weather'][0]['description'];
	console.log(weather['weather']);
	descCont.innerText = 'Description: ' + desc;

	var HumidityCont = document.createElement('div');
	var hum = weather['main']['humidity'];
	HumidityCont.innerText = 'Humidity: ' + hum;

	mainInfo.appendChild(cityCont);
	mainInfo.appendChild(tempCont);
	mainInfo.appendChild(descCont);
	mainInfo.appendChild(HumidityCont);

	// console.log(temp);
}

/* AJAX Boilerplate */
function makeRec(method, target, handlerAction, data) {
	var httpRequest = new XMLHttpRequest();

	if (!httpRequest) {
		alert('Giving up :( Cannot create an XMLHTTP instance');
		return false;
	}

	httpRequest.onreadystatechange = function() {
		if (httpRequest.readyState === XMLHttpRequest.DONE) {
			console.log('DONEDONEDONE');
			handlerAction(httpRequest);
		}
	};
	httpRequest.open(method, target);

	if (data) {
		httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
		httpRequest.send(data);
	} else {
		httpRequest.send();
	}
}
