function hidePagination() {
    $('.pagination').dataTable({
        "fnDrawCallback": function(oSettings) {
            if (oSettings._iDisplayLength > oSettings.fnRecordsDisplay()) {
                $(oSettings.nTableWrapper).find('.dataTables_paginate').hide();
            } else {
                 $(oSettings.nTableWrapper).find('.dataTables_paginate').show();
            }
        }
    });
}


// function showHidePagination() {
//     if(document.getElementsByClassName('pagination').length <= 15) {
//         document.getElementById('pagination').style.display='none';
//     } else {
//         document.getElementById('pagination').style.display='block';
//     }
// }