var updatebuttons = document.getElementsByClassName('update-cart');
console.log(updatebuttons); // This will log an HTMLCollection

for ( var i = 0; i < updatebuttons.length; i++) {
    updatebuttons[i].addEventListener('click', function() {
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log("ProductId:", productId , "Action:", action);
        console.log("user",user);

        if(user == "AnonymousUser"){
            console.log("User is not logged in ...");
        }
        else{
            updateUserOrder(productId, action);
        }
    });
}

// codes for handling registered user add to carts
function updateUserOrder(productId, action) {
    console.log("User is logged in sending data...");
    var url = '/update_item/';

    fetch(url, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({"productId": productId, "action": action}),
    })
    .then((response) => {
        if (!response.ok) {
            throw new Error(response.statusText);
        }
        return response.json();
    })
    .then((data) => {
        console.log("data", data);
        location.reload();
    })
    .catch((error) => {
        console.error("Error updating order:", error);
    });
}