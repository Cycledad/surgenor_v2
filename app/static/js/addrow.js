$(document).ready(function ()
{

//re-worked with Nathan's help. Increased the length of part desc input as per kevin.
debugger;
    var counter = 0;

    $("#addrow").on("click", function ()
    {
       // debugger;
        var newRow = $("<tr>");
        var cols = '<div class="container p-0 m-0"><div class="row">';

        var selectSupplier = '';
        selectSupplier = '<div class="col-2"><div class="input-group mb-3"><select name="selectSupplier' + counter + '" data-supplier class=\'form-control\' id="selectSupplier' + counter + '" required>';
        debugger;
        if (document.getElementById("lang").innerHTML == 'en-us'){
            selectSupplier += '<option value="">-- Supplier --</option>';
        }
        else {
            selectSupplier += '<option value="">-- fournisseur --</option>';
        }
        //selectSupplier += '<option value="">-- Supplier --</option>';
        for (var i = 1; i < document.getElementById('selectSupplier').length; i++)
            {
                selectSupplier += '<option value="' + document.getElementById("selectSupplier").options[i].text + '">' + document.getElementById("selectSupplier").options[i].text + '</option>';
            }
        selectSupplier += '</select></div></div>';
        cols += selectSupplier;

        cols += '<div class="col-1"><div class="input-group mb-3"><input type="number" step="0" min=0 class="form-control" name="quantity' + counter + '" id="quantity' + counter + '"/></div></div>';


        //var partNbr = '';
        //partNbr = '<div class="col-2"> <div class="input-group mb-3"><input type="text" name="partNbr' + counter + '" id="partNbr' + counter + '" class="form-control" required /></div></div>';
        //PartNbr = '<td><select name="PartNbr' + counter + '" class=\'form-control\'  id="PartNbr' + counter + '" required >';
        //PartNbr += '<option value="">--Please select a part nbr</option>';
        //for (var i = 1; i < document.getElementById('PartNbr').length; i++)
        //{
        //    PartNbr += '<option value="' + document.getElementById("PartNbr").options[i].text + '">' + document.getElementById("PartNbr").options[i].text + '</option>';
        //}
        //PartNbr += '</select></td>';
        //cols += partNbr;


        /*cols += '<td><input type="text" class="form-control" name="description' + counter + '"/></td>';*/
        var partDesc = '';
        partDesc = '<div class="col-6"> <div class="input-group mb-3"><textarea name="desc' + counter + '" id="desc' + counter + '" rows=2 cols=2 class="form-control" required></textarea></div></div>';
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
        cols += '<div class="col-2"><div class="input-group mb-3"><input type="number" step="any" min=0 data-unitPrice class="form-control" required name="unitprice' + counter + '" id="unitprice' + counter + '"/></div></div>';


        /* cols += '<td><input type="text" class="form-control" name="cost' + counter + '" onclick="calculateRow(' + name + ')"/></td>'; */
        //cols += '<td><input type="text" class="form-control" id="cost' + counter + '" name="cost' + counter + '" /></td>';



        if (document.getElementById("lang").innerHTML == 'en-us'){
            msg = 'Delete';
        }
        else {
            msg = 'Supprimer';
        }

        cols += '<div class="col-1"><input type="button" class="ibtnDel btn btn-md btn-danger "  value="' + msg + '"></div></div>';



        //console.log(cols);
        newRow.append(cols);
        //console.log(newRow);
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