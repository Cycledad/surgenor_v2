
// addOrder.html

const toggleRequiredAttribute = () => {
        let supplier = document.getElementById('selectSupplier').value;
        if (supplier.toLowerCase() == 'econo') {
            let el = document.getElementById('unitprice');
            el.toggleAttribute('required');
            console.log(el.value);
        }

}