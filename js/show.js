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
