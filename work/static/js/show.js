/**
 * Created by WZL on 2016/11/14.
 */
 $(window).on("load resize ", function() {
            var scrollWidth = $('.tbl-content').width() - $('.tbl-content table').width();
            $('.tbl-header').css({
                'padding-right': scrollWidth
            });
        }).resize();

$('table tr').each(function(){
            $(this).find('th').first().addClass('first');
            $(this).find('th').last().addClass('last');
            $(this).find('td').first().addClass('first');
            $(this).find('td').last().addClass('last');});
$('table tr').first().addClass('row-first');
$('table tr').last().addClass('row-last');

(function(document) {
    'use strict';

    var LightTableFilter = (function(Arr) {

        var _input;

        function _onInputEvent(e) {
            _input = e.target;
            var tables = document.getElementsByClassName(_input.getAttribute('data-table'));
            Arr.forEach.call(tables, function(table) {
                Arr.forEach.call(table.tBodies, function(tbody) {
                    Arr.forEach.call(tbody.rows, _filter);
                });
            });
        }

        function _filter(row) {
            var text = row.textContent.toLowerCase(),
                val = _input.value.toLowerCase();
            row.style.display = text.indexOf(val) === -1 ? 'none' : 'table-row';
        }

        return {
            init: function() {
                var inputs = document.getElementsByClassName('light-table-filter');
                Arr.forEach.call(inputs, function(input) {
                    input.oninput = _onInputEvent;
                });
            }
        };
    })(Array.prototype);

    document.addEventListener('readystatechange', function() {
        if (document.readyState === 'complete') {
            LightTableFilter.init();
        }
    });

})(document);

(function($) {
            $.fn.heavyTable = function(params) {

                params = $.extend( {
                    startPosition: {
                        x: 1,
                        y: 1
                    }
                }, params);

                this.each(function() {
                    var
                            $hTable = $(this).find('tbody'),
                            i = 0,
                            x = params.startPosition.x,
                            y = params.startPosition.y,
                            max = {
                                y: $hTable.find('tr').length,
                                x: $hTable.parent().find('th').length
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

                    $(document).keydown(function(e){
                        if (e.keyCode == 13) {
                            clearCell();
                            edit(selectCell());
                        } else if (e.keyCode >= 37 && e.keyCode <= 40  ) {

                            clearCell();
                            switch (e.keyCode) {
                                case 37: x--;
                                    break;
                                case 38: y--;
                                    break;
                                case 39: x++;
                                    break;
                                case 40: y++;
                                    break;
                            }
                            selectCell();
                            return false;
                        }
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
