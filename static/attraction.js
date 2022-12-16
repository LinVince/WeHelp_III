function getCurrentURL () {
  return window.location.href
}

function getCurrentAttractionId (fn){
	let url = fn()
	let url_array = url.split('/');
	let url_array_length = url_array.length;
	let attraction_id = url_array[url_array_length - 1];
	return attraction_id
}

async function getApiData(){
	const url = getCurrentURL()
	console.log(url)
	let url_array = url.split('/');
	console.log(url_array);
	let url_array_length = url_array.length;
	console.log(url_array_length);
	let attraction_id = url_array[url_array_length - 1];
	console.log(attraction_id);
	var requestURL = "/api/attraction/" + attraction_id;
	isLoading = true;
	const getData = await fetch(requestURL).then(function(response){
		
		return response.json();
	}).then(function(data){
		console.log(data);
		isLoading = false;
		return data;
	})	
		return getData;
};


var image_num = null;
var images = [];

getApiData().then((data) => {
	console.log(data);
	let image = data.data.images[0];
	
	for(let i = 0; i < data.data.images.length; i++){
		let li = data.data.images[i].split('.');
		console.log(li);
		let len = li.length;
		if(li[len - 1] === 'jpg' || li[len - 1] === 'JPG' || li[len - 1] === 'png' || li[len - 1] ==='PNG' ){
			console.log(li[len-1]);
			images.push(data.data.images[i]);
		}else{console.log('Hmm')}
	}	
	console.log(images);
	image_num = images.length;
	console.log(image_num);
	let name = data.data.name;
	console.log(name);
	let attraction_name = document.querySelector('#attraction_name');
	attraction_name.innerText = name;
	let category = data.data.category;
	let mrt = data.data.mrt;
	let cat_and_mrt_ele = document.getElementById('cat_and_mrt');
	cat_and_mrt_ele.innerText = category + ' at ' + mrt;
	let description = data.data.description;
	let description_ele = document.getElementById('description');
	description_ele.innerText = description;
	let address_ele = document.getElementById('address');
	let transportation_ele = document.getElementById('transportation');
	let address = data.data.address;
	let transportation = data.data.transport;
	address_ele.innerText = address;
	transportation_ele.innerText = transportation;
	const thumbnail_frame = document.querySelector('.thumbnail_frame');
	
	for(let i = 0; i < image_num; i++ ){
		let thumbnail = document.createElement('div');
		thumbnail.setAttribute('class','thumbnail');
		thumbnail_frame.appendChild(thumbnail);
		if(i === 0){
			thumbnail.classList.add('thumbnail_active');
		};
	};

	const gallery_slideshow = document.querySelector('.gallery_slideshow');
	for(let i = 0; i < image_num; i++ ){
		let image = document.createElement('img');
		image.setAttribute('src',images[i]);
		image.classList.add("slideshow_photo");
		gallery_slideshow.appendChild(image);
		if(i === 0){
			image.classList.add('slideshow_photo_active');
		}
	}

});

var currentImg = 0;
const prev_btn = document.querySelector('.prev');
const next_btn = document.querySelector('.next');
const image_eles = document.getElementsByClassName('slideshow_photo');
const thumbnail_eles = document.getElementsByClassName('thumbnail');

prev_btn.addEventListener('click',function(){
	if(currentImg === 0){
		console.log('Already the first');
	}else if(image_num > currentImg > 0){
		image_eles[currentImg].classList.remove('slideshow_photo_active');
		thumbnail_eles[currentImg].classList.remove('thumbnail_active');
		currentImg = currentImg - 1;
		image_eles[currentImg].classList.add('slideshow_photo_active');
		thumbnail_eles[currentImg].classList.add('thumbnail_active');

	} 

});

next_btn.addEventListener('click', function(){
	console.log(image_eles);
	if(currentImg === image_num - 1){
		console.log('Already the last');
	}else if(currentImg < image_num - 1){
		console.log(thumbnail_eles);
		image_eles[currentImg].classList.remove('slideshow_photo_active');
		thumbnail_eles[currentImg].classList.remove('thumbnail_active');
		currentImg = currentImg + 1;
		image_eles[currentImg].classList.add('slideshow_photo_active');
		thumbnail_eles[currentImg].classList.add('thumbnail_active');
	}

});

let tour_times = document.querySelectorAll('input[name="tour_time"]');
tour_times.forEach((ele) => {
	ele.addEventListener('change', function(e){
		if(e.target.value === 'morning'){
			document.getElementById('fee').innerText = "新台幣 2000 元";
		}else{document.getElementById('fee').innerText = "新台幣 2500 元"}
	})
});


//Click link to get Login or Signup Popup window
const login_signup_link = document.getElementById("login_signup_link")
const popup_window_login = document.getElementById("popup_window_login")
const popup_window_signup = document.getElementById("popup_window_signup")
const popup_layout = document.querySelector("#popup_layout")
login_signup_link.addEventListener('click',function(){
	popup_window_login.style.display = 'flex'
	popup_layout.style.display = 'block'
	const signup_link = document.getElementById("signup_link")
	signup_link.addEventListener('click', function(){
		popup_window_login.style.display = 'none'
		popup_window_signup.style.display = 'flex'
	});
	const login_link = document.getElementById("login_link")
	login_link.addEventListener('click', function(){
		popup_window_signup.style.display = 'none'
		popup_window_login.style.display = 'flex'
	});
});


// Go back to the front page without any popup window
function goToFront(){
	popup_window_login.style.display = 'none'
	popup_window_signup.style.display = 'none' 
	popup_layout.style.display = 'none'
	reload();
}


// Pop the login window
function signinWindow(){
	popup_window_login.style.display = 'flex'
	popup_layout.style.display = 'block'
	let signup_link = document.getElementById("signup_link")
	signup_link.addEventListener('click', function(){
		popup_window_login.style.display = 'none'
		popup_window_signup.style.display = 'flex'
	});
	let login_link = document.getElementById("login_link")
	login_link.addEventListener('click', function(){
		popup_window_signup.style.display = 'none'
		popup_window_login.style.display = 'flex'
	});
}


// Reload the page
function reload(){
	location.reload();
}


//Define the login function
async function login(){	
	let requestURL = "/api/user/auth";
	let email = document.getElementById('login_email').value
	let password = document.getElementById('login_password').value
	let obj = {"email": email, "password": password};
	console.log(obj)
	//Please write the following line to set your jsondata..otherwise....
  json_data = JSON.stringify(obj);
	const get_response = await fetch(requestURL,{
		method:'PUT',
		headers:{'Content-type':'application/json'},
		body:json_data,
	});
	return get_response.json();
};

//Define the logout function
async function signup(){	
	let requestURL = "/api/user";
	let name = document.getElementById('signup_name').value
	let email = document.getElementById('signup_email').value
	let password = document.getElementById('signup_password').value
	let obj = {"name": name, "email": email, "password": password};
	console.log(obj)
	//Please write the following line to set your jsondata..otherwise....
  json_data = JSON.stringify(obj);
	const get_response = await fetch(requestURL,{
		method:'POST',
		headers:{'Content-type':'application/json'},
		body:json_data,
	});
	return get_response.json();
};

//Login process
const login_button = document.getElementById('login_button')
const login_message = document.getElementById('login_message')
login_button.addEventListener('click',function(){
	login().then((data => {
		if (data.error === true){
			login_message.innerText = data.message;
		}else{
			login_message.innerText = "成功登入"
			setTimeout(goToFront, 1000);
			setTimeout(reload, 1400);
		}
	}));
})

//Logout process
const signup_button = document.getElementById('signup_button')
const signup_message = document.getElementById('signup_message')
signup_button.addEventListener('click',function(){
	signup().then((data => {
		if (data.error === true){
			signup_message.innerText = data.message;
		}else{
			signup_message.innerText = "註冊成功";
			setTimeout(goToFront, 1000);
			setTimeout(reload, 1400);
		}
	}));
})

//Check if the user has logged into the system
async function checkUserLogin(){
	let requestURL = "/api/user/auth";
	const getData = await fetch(requestURL,
	{	method:'GET',
		headers:{'Content-type':'application/json'}
	}).then(function(response){
		return response.json();
	}).then(function(data){
		console.log(data);
		return data;
	})	
		return getData;
};


function afterLogout(){
	login_signup_link.style.display = 'block'
	logout_link.style.display = 'none'
}

function afterLogin(){
	login_signup_link.style.display = 'none'
	logout_link.style.display = 'block'
}

window.addEventListener("load", function(){
	checkUserLogin().then((data) => {
		if(data.data.id != null){
			afterLogin();
			}else{afterLogout()
			} 
	})
  console.log("page is fully loaded");
});


//Logout the user

async function userLogout(){
	let requestURL = "/api/user/auth";
	const getData = await fetch(requestURL,
	{	method:'DELETE',
		headers:{'Content-type':'application/json'}
	}).then(function(response){
		return response.json();
	}).then(function(data){
		console.log(data);
		return data;
	})	
		return getData;
};


const logout_link = document.getElementById('logout_link')
logout_link.addEventListener('click',function(){
	userLogout().then((data) => {
		location.reload();
	})
})



//Close icon close the popup window
const icon_closes = document.querySelectorAll('#icon_close')
icon_closes.forEach(function(btn){
	btn.addEventListener('click',function(){
	goToFront();
	})
})


//Go to the front page (clicking title)
const title = document.getElementById('title')
title.addEventListener('click',function(){
	window.location.href = '/';
});


// Create the function to post the booking information to the server
async function postBookingInfo(attraction_id, tour_date, tour_time, price){
	let obj = {"attractionId": attraction_id,
						  "date": tour_date,
						  "time": tour_time,
						  "price": price
						};
	let requestURL = "/api/booking"
	let json_data = JSON.stringify(obj);
	const get_response = await fetch(requestURL,{
		method:'POST',
		headers:{'Content-type':'application/json'},
		body:json_data,
	});
	return get_response.json();
};


// Click the booking button and then post booking info into db
const booking_btn = document.getElementById('book_btn')
booking_btn.addEventListener('click', function(){
	let tour_date = document.getElementById("tour_date").value
	let tour_time = document.querySelector("input[type='radio'][name=tour_time]:checked").value
	// Extract the number from String
	let numberPattern = /\d+/g;
	let tour_price = document.getElementById('fee').innerText.match(numberPattern).join('')
	// Get the attraction_id
	let attraction_id = getCurrentAttractionId(getCurrentURL)
	checkUserLogin().then((data) => {
	if(data.data.id != null){
			postBookingInfo(attraction_id, tour_date, tour_time, tour_price).then((data) => {
			console.log(data);
			if(data['ok'] == true){
				window.location.href = '/booking'
			}else{console.log('Failed')}
	});
	
	}else{signinWindow()			
			} 
	})				
});

// Make the booking link procedure
const booking_link = document.getElementById("booking_link") 

booking_link.addEventListener('click',function(){
	checkUserLogin().then((data) => {
		if(data.data.id != null){
			window.location.href = '/booking';
		}else{signinWindow();
		}
	})
})