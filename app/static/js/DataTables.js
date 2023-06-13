
 var editor; // use a global for the submit and return data rendering in the examples

$(document).ready(function() {})
    //editor = new $.fn.dataTable.Editor( {
    //    "ajax": '/api/data',
    //    "table": "#data",
        //"table": "#data",
        //"fields": [
        //        {"label": "x",
        //         "name": '0'
        //        },
        //        {"label": "x",
        //         "name": '1'
        //        },
        //        {"label": "x",
        //         "name": '2'
        //        },
        //        {"label": "x",
        //         "name": '3'
        //        },
        //        {"label": "x",
        //         "name": '4'
        //        },
        //        {"label": "x",
        //         "name": '5'
        //        },
        //        {"label": "x",
        //         "name": '6'
        //        },
        //        {"label": "x",
        //         "name": '7'
        //    }
        //]
    //} );

    // Edit record
    $('#data').on('click', 'td.editor-edit', function (e) {
        e.preventDefault();

        editor.edit( $(this).closest('tr'), {
            title: 'Edit record',
            buttons: 'Update'
        } );
    } );

    // Delete a record
    $('#data').on('click', 'td.editor-delete', function (e) {
        e.preventDefault();

        editor.remove( $(this).closest('tr'), {
            title: 'Delete record',
            message: 'Are you sure you wish to remove this record?',
            buttons: 'Delete'
        } );
    } );




    //  $('#data').DataTable({
    //    ajax: '/api/data',
    //    columns: [
    //      {data: '0'},
    //      {data: '1'},
    //      {data: '2'},
    //      {data: '3'},
    //      {data: '4'},
    //      {data: '5'},
    //      {data: '6'},
    //      {data: '7'}
    //      ],
    //      });
    //});