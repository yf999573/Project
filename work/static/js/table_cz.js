/**
 * Created by WZL on 2016/12/12.
 */
(function($) {
    $.fn.heavyTable = function(params) {

        params = $.extend( {
            startPosition: {
                x: 1,
                y: 1
            }
        }, params);

        this.each(function() {
            var $hTable, i, x, y;
            $hTable = $(this).find('tbody');
            i = $hTable.find('tr').length;
            x = params.startPosition.x;
            y = params.startPosition.y;
                max = {
                    y: $hTable.find('tr').length,
                    x: $hTable.parent().find('th').length - i
                };

            //console.log(xMax + '*' + yMax);

            function clearCell () {
                content = $hTable.find('.selected input').val();
                $hTable.find('.selected').html(content);
                $hTable.find('.selected').toggleClass('selected');
            }

            function selectCell () {
                if ( y > max.y ) y = max.y;
                if ( x > max.x ) x = max.x;
                if ( y < 1 ) y = 1;
                if ( x < 1 ) x = 1;
                currentCell =
                    $hTable
                        .find('tr:nth-child('+(y)+')')
                        .find('td:nth-child('+(x)+')');
                content = currentCell.html();
                currentCell
                    .toggleClass('selected')
                return currentCell;
            }

            function edit (currentElement) {
                var input = $('<input>', {type: "text"})
                    .val(currentElement.html())
                currentElement.html(input)
                input.focus();
            }

            $hTable.find('td').click( function () {
                clearCell();
                x = ($hTable.find('td').index(this) % (max.x) + 1);
                y = ($hTable.find('tr').index($(this).parent()) + 1);
                edit(selectCell());
            });
        });
    };
})(jQuery);

$(document).ready( function () {
    $('table').heavyTable({
        xPosition: 1,
        yPosition: 1
    });
});


