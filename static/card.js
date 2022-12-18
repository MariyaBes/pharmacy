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