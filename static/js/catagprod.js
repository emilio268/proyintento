let products = {
	data: [
	  {
		productName: "Regular White T-Shirt",
		category: "Topwear",
		price: "30",
		image: "static/images/pika.png",
	  },
	  {
		productName: "Beige Short Skirt",
		category: "Bottomwear",
		price: "49",
		image: "static/images/pika.png",
	  },
	  {
		productName: "Sporty SmartWatch",
		category: "Watch",
		price: "99",
		image: "static/images/pika.png",
	  },
	  {
		productName: "Basic Knitted Top",
		category: "Topwear",
		price: "29",
		image: "static/images/pika.png",
	  },
	  {
		productName: "Black Leather Jacket",
		category: "Jacket",
		price: "129",
		image: "static/images/pika.png",
	  },
	  {
		productName: "Stylish Pink Trousers",
		category: "Bottomwear",
		price: "89",
		image: "static/images/pika.png",
	  },
	  {
		productName: "Brown Men's Jacket",
		category: "Jacket",
		price: "189",
		image: "static/images/pika.png",
	  },
	  {
		productName: "Comfy Gray Pants",
		category: "Bottomwear",
		price: "49",
		image: "static/images/pika.png",
	  },
	],
  };
  
  for (let i of products.data) {
    let card = document.createElement("div");
    card.classList.add("card", i.category, "hide");

    let imgContainer = document.createElement("div");
    imgContainer.classList.add("image-container");

    let image = document.createElement("img");
    image.setAttribute("src", i.image);
    imgContainer.appendChild(image);
    card.appendChild(imgContainer);

    let container = document.createElement("div");
    container.classList.add("container");

    let name = document.createElement("h5");
    name.classList.add("product-name");
    name.innerText = i.productName.toUpperCase();
    container.appendChild(name);

    let price = document.createElement("h6");
    price.innerText = "$" + i.price;
    container.appendChild(price);

    let viewMoreButton = document.createElement("button");
    viewMoreButton.innerText = "Ver Más";
    viewMoreButton.classList.add("button-ver-mas");
    viewMoreButton.addEventListener("click", function () {
        // Redirigir a la página de detalles del producto con un parámetro
        window.location.href = "detalles_producto.html?producto=" + encodeURIComponent(i.productName);
    });

    container.appendChild(viewMoreButton);
    card.appendChild(container);
    document.getElementById("products").appendChild(card);
}
  
  //parameter passed from button (Parameter same as category)
  function filterProduct(value) {
	//Button class code
	let buttons = document.querySelectorAll(".button-value");
	buttons.forEach((button) => {
	  //check if value equals innerText
	  if (value.toUpperCase() == button.innerText.toUpperCase()) {
		button.classList.add("active");
	  } else {
		button.classList.remove("active");
	  }
	});
  
	//select all cards
	let elements = document.querySelectorAll(".card");
	//loop through all cards
	elements.forEach((element) => {
	  //display all cards on 'all' button click
	  if (value == "all") {
		element.classList.remove("hide");
	  } else {
		//Check if element contains category class
		if (element.classList.contains(value)) {
		  //display element based on category
		  element.classList.remove("hide");
		} else {
		  //hide other elements
		  element.classList.add("hide");
		}
	  }
	});
  }
  
  //Search button click
  document.getElementById("search").addEventListener("click", () => {
	//initializations
	let searchInput = document.getElementById("search-input").value;
	let elements = document.querySelectorAll(".product-name");
	let cards = document.querySelectorAll(".card");
  
	//loop through all elements
	elements.forEach((element, index) => {
	  //check if text includes the search value
	  if (element.innerText.includes(searchInput.toUpperCase())) {
		//display matching card
		cards[index].classList.remove("hide");
	  } else {
		//hide others
		cards[index].classList.add("hide");
	  }
	});
  });
  
  //Initially display all products
  window.onload = () => {
	filterProduct("all");
  };