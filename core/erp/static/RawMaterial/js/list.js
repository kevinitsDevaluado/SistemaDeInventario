$(function () {
    $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "id"},
            {"data": "prov.names"},
            {"data": "nombre"},
            {"data": "uMedida"},
            {"data": "cant"},
            {"data": "descripcion"},
            {"data": "id"}, 
        ],
        columnDefs: [
            
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/erp/rawmaterial/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/erp/rawmaterial/delete/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    //buttons += '<a href="/erp/cargarRawMaterial/add/" type="button" style="margin-left: 4px" class="btn btn-success btn-xs btn-flat"><i class="fa fa-plus-square"></i></a>';
                    
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
});
