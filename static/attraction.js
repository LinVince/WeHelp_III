function getCurrentURL () {
  return window.location.href
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
		if(e.target.value === 'day'){
			document.getElementById('fee').innerText = "新台幣 2000 元";
		}else{document.getElementById('fee').innerText = "新台幣 2500 元"}
	})
});