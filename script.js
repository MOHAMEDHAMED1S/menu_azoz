const jsonFile = 'products.json'; // ملف المنتجات

// تحميل المنتجات
async function loadProducts() {
    const response = await fetch(jsonFile);
    const products = await response.json();
    return products;
}

// عرض المنتجات في المنيو
async function displayMenu() {
    const products = await loadProducts();
    const menu = document.getElementById("menu");


    products.forEach(product => {
        // إنشاء العنصر li
        const listItem = document.createElement("li");
        listItem.classList.add("appItem");
        listItem.setAttribute("data-ingredients", "chicken, seasoning"); // يمكنك تعديل هذه القيمة حسب الحاجة
      
        // إضافة المحتوى داخل العنصر li
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
      
        // إضافة العنصر إلى القائمة
        menu.appendChild(listItem);
      });
}






// ربط الوظائف مع الأحداث
if (document.getElementById('menu')) {
    displayMenu();
}
