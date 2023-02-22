
// addOrder.html - econo supplier does not require a price, all other supplier require price to be entered

const toggleRequiredAttribute = () => {

        const supplierElements = document.querySelectorAll('[data-supplier]');
        const priceElements = document.querySelectorAll('[data-unitPrice]');

        let count = 0;
        //debugger;
        supplierElements.forEach((el) => {
            //console.log('count = ' + count);
            //console.log(el.value);
            if (el.value.toLowerCase() == 'econo') {
                //console.log(priceElements[count].required);
                priceElements[count].required = false;
                //console.log(priceElements[count].required);
                //priceElements[count].toggleAttribute('required');
                //console.log('toggle');
            }
            count += 1;
        });
}