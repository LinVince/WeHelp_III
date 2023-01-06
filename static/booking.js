// Define the element at the top (for login/logout/title)
const login_signup_link = document.getElementById("login_signup_link")
const popup_window_login = document.getElementById("popup_window_login")
const popup_window_signup = document.getElementById("popup_window_signup")
const popup_layout = document.querySelector("#popup_layout")
const signup_link = document.getElementById("signup_link")
const login_link = document.getElementById("login_link")
const logout_link = document.getElementById('logout_link')
const login_button = document.getElementById('login_button')
const login_message = document.getElementById('login_message')
const signup_button = document.getElementById('signup_button')
const signup_message = document.getElementById('signup_message')
const booking_link = document.getElementById('booking_link')
const title = document.getElementById('title')

// Greeting words
const greeting_heading = document.querySelector('.greeting_heading')

// No_booking_info_node
const no_booking_info = document.getElementById('no_booking_info')

// Define the element of the information about the attraction
const attraction_photo = document.getElementById('attraction_photo')
const attraction_name = document.getElementById('attraction_name')
const attraction_date = document.getElementById('attraction_date')
const attraction_time = document.getElementById('attraction_time')
const attraction_price = document.getElementById('attraction_price')
const attraction_address = document.getElementById('attraction_address')

// Define the icon element (delete the booking)
const booking_del_btn = document.getElementById('booking_delete_btn')

// Define the elements to be deleted if there isn't any booking info
const containers_to_be_del = document.querySelectorAll('.container')
const flex_centers = document.querySelectorAll('.flex_center')

// Define the element at the bottom
const total_price = document.getElementById('total_price')
const confirm_booking_bill_btn = document.getElementById('confirm_booking_bill_btn')

//footer
const footer = document.querySelector('.footer')





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

// Render greeting heading
async function renderGreeting(){
	let requestURL = "/api/user/auth";
	const getData = await fetch(requestURL,
	{	method:'GET',
		headers:{'Content-type':'application/json'}
	}).then(function(response){
		return response.json();
	}).then(function(data){
		console.log(data)
		greeting_heading.innerText = "您好，" + data.data.name + "，您的行程如下："
		return data;
	})	
		return getData;
};

// Get the information from api/booking if logged in
async function getBookingInfo(){
	let requestURL = "/api/booking";
	let getData = await fetch(requestURL,
	{	method:'GET',
		headers:{'Content-type':'application/json'}
	}).then(function(response){
		return response.json();
	}).then(function(data){
		return data	
	})	
		return getData;
};

// Render the information retrieved from api/booking if logged in
async function renderBookingInfo(){
	let requestURL = "/api/booking";
	let getData = await fetch(requestURL,
	{	method:'GET',
		headers:{'Content-type':'application/json'}
	}).then(function(response){
		return response.json();
	}).then(function(data){
		if(data.data.attraction.id != null){
		attraction_photo.setAttribute('src',data.data.attraction.image);
		attraction_name.innerText = data.data.attraction.name;
		attraction_date.innerText = data.data.date;
		if(data.data.time === 'morning'){
			attraction_time.innerText = "早上 9 時到下午 4 時";
		}else{attraction_time.innerText = "下午 4 時到晚上 7 時"}		
		attraction_price.innerText = "新台幣 " + data.data.price + " 元";
		total_price.innerText = attraction_price.innerText
		attraction_address.innerText = data.data.attraction.address;
		}else{noBookingInfoNotice()}	
	})	
		return getData;
};

// Send the "Delete the booking" request to the backend
async function booking_del_request(){
	let requestURL = "/api/booking";
	const getData = await fetch(requestURL,
	{	method:'DELETE',
		headers:{'Content-type':'application/json'},
	}).then(function(response){
		return response.json();
	}).then(function(data){
		console.log(data)
	});

	return getData
}

// Delete all nodes and show "尚無資料可顯示"
function noBookingInfoNotice(){
	containers_to_be_del.forEach(container => {
		container.remove();
	});
	console.log('hey!');
	console.log(flex_centers);
	for(let i = 0; i < flex_centers.length; i++){
		console.log(flex_centers[i])
		if(i > 3){
		flex_centers[i].remove();
		}else{console.log('Pass')}
	};
	no_booking_info.style.display = "flex";
	footer.style.position = 'fixed';
	footer.style.bottom = '0px';
};

// Top-right corner: display login/signup
function afterLogout(){
	login_signup_link.style.display = 'block'
	logout_link.style.display = 'none'
}

// Redirect to the frontpage
function redirectToFrontpage(){
	window.location.href = '/';
}

// Top-right corner: display logout
function afterLogin(){
	login_signup_link.style.display = 'none'
	logout_link.style.display = 'block'
}








//Go to the front page (clicking title)
title.addEventListener('click',function(){
	window.location.href = '/';
});

// if not logged, direct the user to the frontpage
// if logged, greet the usre and render the booking info from (api/booking) or show "no booking"
window.addEventListener("load", function(){
	checkUserLogin().then((data) => {
		if(data.data.id != null){
			afterLogin();
			renderBookingInfo();
			renderGreeting();
			}else{
				afterLogout();
				redirectToFrontpage();
			} 
	})
  console.log("page is fully loaded");
});

// Logout
logout_link.addEventListener('click', function(){
	userLogout();
	window.location.href = '/'
})


// Direct to the booking page after the booking_link is clicked
booking_link.addEventListener('click',function(){
	window.location.href = '/booking'
})

// Delete the booking 
booking_del_btn.addEventListener('click', function(){
	booking_del_request();
	location.reload();
});




//Tappay Transaction 
// call TPDirect.card.getPrime when user submit form to get tappay prime

const pay_btn = document.getElementById('confirm_booking_bill_btn')

//Tappay SDK - get prime and post order to the server

pay_btn.addEventListener('click', function(){
	getBookingInfo().then((data) => {
		// Get the booking info
		let price = data.data.price;
		let date = data.data.date;
		let time = data.data.time;
		let attraction = data.data.attraction;

		// Get the contact info
		let contact_name = document.getElementById('contact_name').value
		let contact_email = document.getElementById('contact_email').value
		let contact_mobile = document.getElementById('contact_mobile').value

		// Get the prime and send POST inside 
		TPDirect.card.getPrime((result) => {
			let prime = result.card.prime

			// Send information (POST) to the server
			let requestURL = "/api/orders";
			let obj = {"prime": prime,
					   "order": {
						    "price": price,
						    "trip": {
						      "attraction": attraction,
						      "date": date,
						      "time": time
						    },
						    "contact": {
						      "name": contact_name,
						      "email": contact_email,
						      "phone": contact_mobile
						    }
						  }
						};
			
			json_data = JSON.stringify(obj);
			console.log(json_data)
			const get_response = fetch(requestURL,{
			method:'POST',
			headers:{'Content-type':'application/json'},
			body:json_data,
			}).then(function(response){
					return response.json();
			}).then(function(data){
				if(data.data.payment.status === 0){
					window.location.href = '/thankyou?number=' + data.data.number;
				};
				
			});	
				return get_response;
		});
	});
});
