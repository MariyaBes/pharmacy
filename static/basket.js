document.addEventListener('DOMContentLoaded', () => {
	const productsBtn = document.querySelectorAll('.product__btn');
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
		document.querySelector(`.product[data-id="${id}"]`).querySelector('.product__btn').disabled = false;
		
		let currentPrice = parseInt(productParent.querySelector('.cart-product__price').textContent);
		console.log(currentPrice)
		minusFullPrice(currentPrice);
		printFullPrice();
		productParent.remove();

		printQuantity();

		updateStorage();
	};

	productsBtn.forEach(el => {

		el.addEventListener('click', (e) => {
			let self = e.currentTarget;
			let parent = self.closest('.product');
			let id = parent.dataset.id;
			console.log(id);
			let img = parent.querySelector('.image-switch__img img').getAttribute('src');
			console.log(img);
			let title = parent.querySelector('.showcase-title').textContent;
			console.log(title);
			
			let priceString = priceWithoutSpaces(parent.querySelector('.price-box .price').textContent);
			console.log(priceString);
			let priceNumber = parseInt(priceWithoutSpaces(parent.querySelector('.price-box .price').textContent));
			console.log(priceNumber);

			
			plusFullPrice(priceNumber);
			printFullPrice();

			cartProductsList.querySelector('.simplebar-content').insertAdjacentHTML('afterbegin', generateCartProduct(img, title, priceString, id));
			printQuantity();

			updateStorage();

			
			self.disabled = true;
		});
	});

	const countSumm = () => {
		document.querySelectorAll('.cart-content__item').forEach(el => {
			price += parseInt(priceWithoutSpaces(el.querySelector('.cart-product__price').textContent));
		});
	};

	const initialState = () => {
		if (localStorage.getItem('products') !== null) {
			cartProductsList.querySelector('.simplebar-content').innerHTML = localStorage.getItem('products');
			printQuantity();

			countSumm();
			printFullPrice();

			document.querySelectorAll('.cart-content__product').forEach(el => {
				let id = el.dataset.id;
				console.log(id)
				document.querySelector(`.product[data-id="${id}"]`).querySelector('.product__btn').disabled = true;
			});
		}
	};

	initialState();

	const updateStorage = () => {
		let parent = cartProductsList.querySelector('.simplebar-content');
		let html = parent.innerHTML;
		html = html.trim();
		console.log(html);

		if (html.length) {
			localStorage.setItem('products', html);
		}
		else {
			localStorage.removeItem('products');
		}
		
	};

	cartProductsList.addEventListener('click', (e) => {
		if (e.target.classList.contains('cart-product__delete')) {
			deleteProducts(e.target.closest('.cart-content__item'));
		}
	});
});