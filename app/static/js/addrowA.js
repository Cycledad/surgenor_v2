$(document).ready(function () {
    var counter = 0;




    $("#addrow").on("click", function () {


        var newRow = $("<tr>");
        var cols = "";


        var selectPartNbr = '';
        selectPartNbr = '<td><select name="selectPartNbr' + counter + '" class=\'form-control\'  id="selectPartNbr' + counter + '" required >';
        selectPartNbr += '<option value="">--Please select a part nbr</option>';
             for (var i = 1; i < document.getElementById('selectPartNbr').length; i++) {
                 selectPartNbr += "<option value='" + document.getElementById("selectPartNbr").options[i].text + '>" + document.getElementById("selectPartNbr").options[i].text + '</option>';
             }
        selectPartNbr += '</select></td>';
        cols += selectPartNbr;

        /*cols += '<td><input type="text" class="form-control" name="description' + counter + '"/></td>';*/
        var selectPartDesc = '';
        selectPartDesc = '<td><select name="selectPartDesc' + counter + '" class=\'form-control\' id="selectPartDesc' + counter + '" required >';
        selectPartDesc += '<option value="">--Please select part description</option>';
             for (var i = 1; i < document.getElementById('selectPartDesc').length; i++) {
                 selectPartDesc += "<option value='" + document.getElementById("selectPartDesc").options[i].text + '">" + document.getElementById("selectPartDesc").options[i].text + '</option>';
             }
        selectPartDesc += '</select></td>';
        cols += selectPartDesc;



        /* cols += '<td><input type="text" class="form-control" name="supplier' + counter + '"/></td>'; */

        var selectSupplier = '';
        selectSupplier = '<td><select name="selectSupplier' + counter + '" class=\'form-control\' id="selectSupplier' + counter + '" required >';
        selectSupplier += '<option value="">--Please select supplier</option>';
             for (var i = 1; i < document.getElementById('selectSupplier').length; i++) {
                 selectSupplier += "<option value='" + document.getElementById("selectSupplier").options[i].text + '">" + document.getElementById("selectSupplier").options[i].text + '</option>';
             }
        selectSupplier += '</select></td>';
        cols += selectSupplier;




        cols += '<td><input type="text" class="form-control" name="quantity' + counter + '" id="quantity' + counter + '"/></td>';

        /* cols += '<td><input type="text" class="form-control" name="unit' + counter + '"/></td>'; */

        var selectUnit = '';
        selectUnit = '<td><select name="selectUnit' + counter + '" class=\'form-control\' id="selectUnit' + counter + '" required >';
        selectUnit += '<option value="">--Please select unit</option>';
             for (var i = 1; i < document.getElementById('selectUnit').length; i++) {
                 selectUnit += "<option value='" + document.getElementById("selectUnit").options[i].text + '">" + document.getElementById("selectUnit").options[i].text + '</option>';
             }
        selectUnit += '</select></td>';
        cols += selectUnit;



        cols += '<td><input type="text" class="form-control" name="unitprice' + counter + '" id="unitprice' + counter + '"/></td>';

        /* cols += '<td><input type="text" class="form-control" name="cost' + counter + '" onclick="calculateRow(' + name + ')"/></td>'; */
        cols += '<td><input type="text" class="form-control" id="cost' + counter + '" name="cost' + counter + '" onclick="calculateRow(name)"/></td>';




        cols += '<td><input type="button" class="ibtnDel btn btn-md btn-danger "  value="Delete"></td>';
        console.log(cols);
        newRow.append(cols);
        $("table.order-list").append(newRow);
        counter++;
    });



    $("table.order-list").on("click", ".ibtnDel", function (event) {
        $(this).closest("tr").remove();
        counter -= 1
        calculateGrandTotal();
    });


});



function calculateRow(name) {

    var q = 'quantity';
    var u = 'unitprice';

    let len = name.length;
    if (len > 4) {
        nbr = name.slice(4, len);
        q = 'quantity' + nbr;
        u = 'unitprice' + nbr;
        console.log('q: ' + q)
        console.log('u: ' + u)

    }
    console.log('name: ' + name)
    console.log('document.getElementById(q).value => ' + document.getElementById(q).value);
    console.log('document.getElementById(u).value => ' + document.getElementById(u).value);

    var r = document.getElementById(q).value * document.getElementById(u).value;
    console.log('document.getElementById(r).value => ' + r);


    document.getElementById(name).value = r;
    //document.getElementById(name).innerHTML = r;

    console.log('just b4 calling calc');
    calculateGrandTotal();
    console.log('just after calling calc');

    /* var cost =+ row.find('input[name^="cost"]').val();*/



}

function calculateGrandTotal() {
    console.log('inside grand total');
    var total = 0;
    $("table.order-list").find('input[name^="cost"]').each(function () {
        total += +$(this).val();
        console.log(total);
    });
    //$("#grandtotal").text(grandtotal.toFixed(2));
    //$("#grandtotal").innerHTML = grandtotal;
    document.getElementById('grandtotal').value = total;

}