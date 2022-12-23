document.addEventListener('DOMContentLoaded', () => {
	const productsBtn = document.querySelectorAll('.product__btn');
	const cartProductsList = document.querySelector('.cart-content__list');
	const cart = document.querySelector('.cart');
	const cartQuantity = cart.querySelector('.count');
	const fullPrice = document.querySelector('.fullprice');
	let idProduct = document.getElementById(['data-id']);
	
	const count = document.querySelector('.items_current');
	let price = 0;
	let id_item = document.querySelector('.del_id_item').getAttribute('id');
	console.log(id_item);

	const priceWithoutSpaces = (str) => {
		return str.replace(/\s/g, '');
	};

	const normalPrice = (str) => {
		return String(str).replace(/(\d)(?=(\d\d\d)+([^\d]|$))/g, '$1 ');
	};

	const plusFullPrice = (totalCount) => {
		return price += totalCount;
	};

	const totalPriceCount = (counter, currentPrice) => {
		totalCount = counter * currentPrice;
		return plusFullPrice (totalCount);
	}

	const minusFullPrice = (currentPrice) => {
		return price -= currentPrice;
	};

	const totalPriceMinusCount = (counter, currentPrice) => {
		totalCount = counter / currentPrice;
		return minusFullPrice (totalCount);
	}


	const printFullPrice = () => {
		fullPrice.textContent = `${normalPrice(price)} ₽`;
	};

	// const deleteProducts = (productParent) => {
	// 	let id = productParent.querySelector('.cart-product').dataset.id;
	// 	document.querySelector(`.product[data-id="${id}"]`).querySelector('.product__btn').disabled = false;
		
	// 	let currentPrice = parseInt(productParent.querySelector('.cart-product__price').textContent);
	// 	console.log(currentPrice)
	// 	minusFullPrice(currentPrice);
	// 	printFullPrice();
	// 	productParent.remove();

	// 	printQuantity();

	// 	// updateStorage();
	// };

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
			let counter = parent.querySelector('[data-counter]').textContent;
			console.log(counter);
			
			let priceString = priceWithoutSpaces(parent.querySelector('.price-box .price').textContent);
			console.log(priceString);
			let priceNumber = parseInt(priceWithoutSpaces(parent.querySelector('.price-box .price').textContent));
			console.log(priceNumber);

			totalPriceCount(counter, priceNumber);
			// plusFullPrice(priceNumber);
			printFullPrice();
			let fullPrice = totalPriceCount(counter, priceNumber)
			console.log(fullPrice);

			// cartProductsList.querySelector('.simplebar-content').insertAdjacentHTML('afterbegin', generateCartProduct(img, title, priceString, id, counter));
			printQuantity();

			// updateStorage();

			
			self.disabled = true;

			$.ajax({
				url: '/basket',
				method: 'post',
				dataType: 'json',
				data: {
					id: id,
					img: img,
					title: title,
					price: priceNumber,
					count: counter
				},
				success: function (response) {
					console.log(response);
				},
				error: function (error) {
					console.log(error);
				}
			});

		});
	});

	// cartProductsList.addEventListener('click', (e) => {
	// 	if (e.target.classList.contains('cart-product__delete')) {
	// 		deleteProducts(e.target.closest('.cart-content__item'));
	// 	}
	// });


	// Добавляем прослушку на всем окне
	window.addEventListener('click', function (event) {

		let counter;

		if (event.target.dataset.action === 'plus' || event.target.dataset.action === 'minus') {

			const counterWrapper = event.target.closest('.counter-wrapper');
			counter = counterWrapper.querySelector('[data-counter]');
		}

		if (event.target.dataset.action === 'plus') {
			if (counter.innerText < 10){
				counter.innerText = ++counter.innerText;
			}
		}

		if (event.target.dataset.action === 'minus') {

			if (parseInt(counter.innerText) > 1) {
				counter.innerText = --counter.innerText;
			} 
		}
	});
});

