async function getApiData(page_num, keyword){
	page_num = String(page_num);
	var requestURL = "/api/attractions?page=" + page_num + "&keyword=" + keyword;
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

async function getApiCat(){
	let requestURL = "/api/categories";
	const getData = await fetch(requestURL).then(function(response){
		return response.json();
	}).then(function(data){
		console.log(data);
		return data;
	})
		return getData;
};

function render(){
	for(var i = 0; i < data_array.length; i++){
	let container = document.querySelector('.container');
	let grid_item = document.createElement('div');
	grid_item.setAttribute('class','gallery__img');
	container.appendChild(grid_item);

	let a = document.createElement('a');
	let id = data_array[i].id;
	a.setAttribute('href','/attraction/' + String(id));

	let img = document.createElement('img');
	img.setAttribute('src',data_array[i].images[0]);
	a.appendChild(img);
	grid_item.appendChild(a);

	let desc_bar = document.createElement('div');
	desc_bar.classList.add("desc_bar");
	grid_item.appendChild(desc_bar);  

	let MRT = document.createElement('span');
	MRT.textContent = data_array[i].mrt;
	desc_bar.appendChild(MRT);

	let CAT = document.createElement('span');
	CAT.textContent = data_array[i].category;
	desc_bar.appendChild(CAT);
	CAT.setAttribute('style','margin-right:15px');
	MRT.setAttribute('style','margin-left: 10px');

	let name_bar = document.createElement('div');
	name_bar.classList.add("name_bar");
	grid_item.appendChild(name_bar);

	let NM = document.createElement('span');
	NM.innerText = data_array[i].name;
	NM.setAttribute('style','margin-left: 10px; font-size:16px; margin-top:3px;');
	name_bar.appendChild(NM);
}
};

var data_array = [];
var next_page = null;
var keyword = '';
var isLoading = false;
var categories = []

getApiData(0,'').then((data) => {
	data_array = data.data;
	next_page = data.next_page;
	console.log(data_array);
	console.log(next_page);
	render();
});

getApiCat().then((data) => {
	categories = data.data;
	console.log(categories);
	for(var i = 0; i < categories.length; i++){
	let category_box = document.getElementById('search_category');
	let category_item = document.createElement('div');
	console.log("hello");
	category_item.classList.add("item_category");
	console.log(category_item);
	category_box.appendChild(category_item);
	category_item.innerText = categories[i];
};
});


window.addEventListener('scroll', throttle(callback, 0));

function throttle(fn, wait) {
  var time = Date.now();
  return function() {
    if ((time + wait - Date.now()) < 0) {
      fn();
      time = Date.now();
    }
  }
}

function callback() {
  let container = document.querySelector(".container");
  console.log(container.getBoundingClientRect().bottom, window.innerHeight);
  if (container.getBoundingClientRect().bottom <= window.innerHeight ) {
	console.log("元素底端已進入畫面");
	if (next_page != null && isLoading === false){	
		getApiData(next_page,keyword).then((data) => {
		data_array = data.data;
		next_page = data.next_page;
		console.log(data_array);
		console.log(next_page);
		render();
	});
	} else{
		console.log('no more pages')
	}
};
};

function removeAllChildNodes(parent) {
    while (parent.firstChild) {
        parent.removeChild(parent.firstChild);
    }
}

const search_btn = document.getElementById('search_icon');
const search_input = document.getElementById('search_input');
const search_category = document.getElementById('search_category');
search_btn.addEventListener('click', function(){
	let container = document.querySelector(".container");
	removeAllChildNodes(container);
	keyword = search_input.value;
	getApiData(0, keyword).then((data) => {
	if(data.error === true){
		console.log('no');
		let container = document.querySelector(".container");
		container.innerText = "沒有資料可以顯示";
	}else{
		data_array = data.data;
		next_page = data.next_page;
		render();
	};
	
});
})

// window.getComputedStyle(search_category).display;
window.addEventListener('click', function(e){
	console.log(e.target.classList.contains('item_category'));
	console.log(e.target);
	if (e.target === search_input){
		search_category.style.display = 'flex';
	}if(e.target != search_input){
		search_category.style.display = 'none';
	}if(e.target.classList.contains('item_category')){
		search_input.value = e.target.innerText;
	}

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


//Go back to the front page without any popup window
function goToFront(){
	popup_window_login.style.display = 'none'
	popup_window_signup.style.display = 'none' 
	popup_layout.style.display = 'none'
}

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
			reload();
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
			reload();
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

