let ProductImg = document.getElementsByClassName('small-img');

let activeImages = document.getElementsByClassName('active');

for(var i=0; i < ProductImg.length; i++){

    ProductImg[i].addEventListener('click', function(){
        console.log(activeImages);

        if(activeImages.length > 0){
            activeImages[0].classList.remove('active')
        }

        this.classList.add('active');
        document.getElementById('ProductImg').src = this.src;
    })
}



const productsBtn = document.querySelectorAll('.cart__btn');
const cartProductsList = document.querySelector('.cart-content__list');
const cart = document.querySelector('.cart');
const cartQuantity = cart.querySelector('.count');
const fullPrice = document.querySelector('.fullprice');
const idProduct = document.querySelector('[data-id]');
let price = 0;

const priceWithoutSpaces = (str) => {
	return str.replace(/\s/g, '');
};

const normalPrice = (str) => {
	return String(str).replace(/(\d)(?=(\d\d\d)+([^\d]|$))/g, '$1 ');
};

const plusFullPrice = (currentPrice) => {
	return price += currentPrice;
};

const minusFullPrice = (currentPrice) => {
	return price -= currentPrice;
};

const printQuantity = () => {
	let productsListLength = cartProductsList.querySelector('.simplebar-content').children.length;
	cartQuantity.textContent = productsListLength;
	productsListLength > 0 ? cart.classList.add('active') : cart.classList.remove('active');
};

const printFullPrice = () => {
	fullPrice.textContent = `${normalPrice(price)} ₽`;
};

const generateCartProduct = (img, title, price, id) => {
	return `
		<li class="cart-content__item">
			<article class="cart-content__product cart-product" data-id="${id}">
				<img src="${img}" alt="" class="cart-product__img">
				<div class="cart-product__text">
				<a href="/cart/${id}">
					<h3 class="cart-product__title">${title}</h3>
				</a>
					<span class="cart-product__price">${normalPrice(price)}</span>
				</div>
				<button class="cart-product__delete" aria-label="Удалить товар"></button>
			</article>
		</li>
	`;
};

const deleteProducts = (productParent) => {
	let id = productParent.querySelector('.cart-product').dataset.id;
	document.querySelector(`.row-cart-product[data-id="${id}"]`).querySelector('.cart__btn').disabled = false;
	
	let currentPrice = parseInt(productParent.querySelector('.cart-product__price').textContent);
	console.log(currentPrice)
	minusFullPrice(currentPrice);
	printFullPrice();
	productParent.remove();

	printQuantity();
};

productsBtn.forEach(el => {

	el.addEventListener('click', (e) => {
		let self = e.currentTarget;
		let parent = self.closest('.row-cart-product');
		let id = parent.dataset.id;
		console.log(id);
		let img = parent.querySelector('.img-container img').getAttribute('src');
		console.log(img);
		let title = parent.querySelector('.col-2').textContent;
		console.log(title);
		
		let priceString = priceWithoutSpaces(parent.querySelector('.Price_price__qHqZv').textContent);
		console.log(priceString);
		let priceNumber = parseInt(priceWithoutSpaces(parent.querySelector('.Price_price__qHqZv').textContent));
		console.log(priceNumber);

		
		plusFullPrice(priceNumber);
		printFullPrice();

		cartProductsList.querySelector('.simplebar-content').insertAdjacentHTML('afterbegin', generateCartProduct(img, title, priceString, id));
		printQuantity();

		
		self.disabled = true;
	});
});

cartProductsList.addEventListener('click', (e) => {
	if (e.target.classList.contains('cart-product__delete')) {
		deleteProducts(e.target.closest('.cart-content__item'));
	}
});