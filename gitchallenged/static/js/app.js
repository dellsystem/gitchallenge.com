$(document).ready(function() {
    $('.skip-to').on('click', function() {
        $('body').scrollTo($(this).attr('href'), 300);
        return false;
    });
});
