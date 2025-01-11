const jsonFile = 'products.json'; 

async function loadProducts() {
    const response = await fetch(jsonFile);
    const products = await response.json();
    return products;
}

async function displayMenu() {
    const products = await loadProducts();
    const menu = document.getElementById("menu");


    products.forEach(product => {
        const listItem = document.createElement("li");
        listItem.classList.add("appItem");
        listItem.setAttribute("data-ingredients", "chicken, seasoning"); // يمكنك تعديل هذه القيمة حسب الحاجة
      
        listItem.innerHTML = `
          ${product.name}  
          <p>${product.description}</p>
          <img src="${product.image}" />
          <span style="
    margin-top: 10px;
    border-top-width: 0px;
    border-right-width: 0px;
    border-left-width: 0px;
    direction: rtl;
">${product.price} جنـية</span>
        `;
      
        menu.appendChild(listItem);
      });
}






// ربط الوظائف مع الأحداث
if (document.getElementById('menu')) {
    displayMenu();
}
