<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
<script type="text/javascript" src="jquery.js"></script>


$(function () {
    $('li a').click(function (e) {
        $('#myModal img').attr('src', $(this).attr('data-img-url'));
    });
});
