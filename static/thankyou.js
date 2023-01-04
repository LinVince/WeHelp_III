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


// Dynamically fill the thankyou info
const thankYouInfo = document.getElementById('thankyou_info')

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
});


// Direct to the booking page after the booking_link is clicked
booking_link.addEventListener('click',function(){
	window.location.href = '/booking'

});



// Fixed the footer
footer.style.position = 'fixed';
footer.style.bottom = '0px';

// Render the frontpage with thankyou message
let params = new URLSearchParams(document.location.search);
let order_number = params.get('number')
thankYouInfo.innerText = '感謝您訂購台北一日遊的導覽行程，您的訂單編號為 ' + order_number + ' 祝您有個美好的行程'




