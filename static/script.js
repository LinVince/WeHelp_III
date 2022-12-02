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



