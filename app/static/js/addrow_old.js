$(document).ready(function ()
{
    var counter = 0;

    $("#addrow").on("click", function ()
    {
        //debugger;
        var newRow = $("<tr>");
        var cols = "";

        var selectSupplier = '';
        selectSupplier = '<td><select name="selectSupplier' + counter + '" class=\'form-control\' id="selectSupplier' + counter + '" required >';
        selectSupplier += '<option value="">--Please select supplier</option>';
             for (var i = 1; i < document.getElementById('selectSupplier').length; i++)
             {
                 selectSupplier += '<option value="' + document.getElementById("selectSupplier").options[i].text + '">' + document.getElementById("selectSupplier").options[i].text + '</option>';
             }
        selectSupplier += '</select></td>';
        cols += selectSupplier;

        cols += '<td><input type="number" step="0" class="form-control" name="quantity' + counter + '" id="quantity' + counter + '"/></td>';


        var partNbr = '';
        partNbr = '<td><input type="text" name="partNbr' + counter + '" id="partNbr' + counter + '" class="form-control" required /></td>';
        //PartNbr = '<td><select name="PartNbr' + counter + '" class=\'form-control\'  id="PartNbr' + counter + '" required >';
        //PartNbr += '<option value="">--Please select a part nbr</option>';
        //for (var i = 1; i < document.getElementById('PartNbr').length; i++)
        //{
        //    PartNbr += '<option value="' + document.getElementById("PartNbr").options[i].text + '">' + document.getElementById("PartNbr").options[i].text + '</option>';
        //}
        //PartNbr += '</select></td>';
        cols += partNbr;


        /*cols += '<td><input type="text" class="form-control" name="description' + counter + '"/></td>';*/
        var partDesc = '';
        partDesc = '<td><input type="text" name="partDesc' + counter + '" id="partDesc' + counter + '" class="form-control" required /></td>';
        //PartDesc = '<td><select name="PartDesc' + counter + '" class=\'form-control\' id="PartDesc' + counter + '" required >';
        //PartDesc += '<option value="">--Please select part description</option>';
        //for (var i = 1; i < document.getElementById('PartDesc').length; i++)
        //{
        //    PartDesc += '<option value="' + document.getElementById("PartDesc").options[i].text + '">' + document.getElementById("PartDesc").options[i].text + '</option>';
        //}
        //PartDesc += '</select></td>';
        cols += partDesc;


        /* cols += '<td><input type="text" class="form-control" name="supplier' + counter + '"/></td>'; */

        /* cols += '<td><input type="text" class="form-control" name="unit' + counter + '"/></td>'; */

        /* as per Kevin Jan 16, 2023, no unit or unit price
        var selectUnit = '';
        selectUnit = '<td><select name="selectUnit' + counter + '" class=\'form-control\' id="selectUnit' + counter + '" required >';
        selectUnit += '<option value="">--Please select unit</option>';
             for (var i = 1; i < document.getElementById('selectUnit').length; i++)
             {
                 selectUnit += '<option value="' + document.getElementById("selectUnit").options[i].text + '">' + document.getElementById("selectUnit").options[i].text + '</option>';
             }
        selectUnit += '</select></td>';
        cols += selectUnit;

    */
        cols += '<td><input type="number" step="0.00" class="form-control" name="unitprice' + counter + '" id="unitprice' + counter + '"/></td>';


        /* cols += '<td><input type="text" class="form-control" name="cost' + counter + '" onclick="calculateRow(' + name + ')"/></td>'; */
        //cols += '<td><input type="text" class="form-control" id="cost' + counter + '" name="cost' + counter + '" /></td>';


        cols += '<td><input type="button" class="ibtnDel btn btn-md btn-danger "  value="Delete"></td>';
        console.log(cols);
        newRow.append(cols);
        $("table.order-list").append(newRow);
        counter++;
    });



    $("table.order-list").on("click", ".ibtnDel", function (event)
    {
        $(this).closest("tr").remove();
        counter -= 1
        //calculateGrandTotal();
    });


});



//function calculateRow(name)
//{
//
//    var q = 'quantity';
//    var u = 'unitprice';
//
//    let len = name.length;
//    if (len > 4) {
//        nbr = name.slice(4, len);
//        q = 'quantity' + nbr;
//        u = 'unitprice' + nbr;
//        console.log('q: ' + q)
//        console.log('u: ' + u)
//
//    }
//    console.log('name: ' + name)
//    console.log('document.getElementById(q).value => ' + document.getElementById(q).value);
//    console.log('document.getElementById(u).value => ' + document.getElementById(u).value);
//
//    var r = document.getElementById(q).value * document.getElementById(u).value;
//    console.log('document.getElementById(r).value => ' + r);
//
//
//    document.getElementById(name).value = r;
    //document.getElementById(name).innerHTML = r;
//
 //   console.log('just b4 calling calc');
 //   calculateGrandTotal();
 //   console.log('just after calling calc');
//
    /* var cost =+ row.find('input[name^="cost"]').val();*/
//
//}



/*
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
*/