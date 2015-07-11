$("body").ready(function() {
    $(".content").each(function() {
        var lq = $('<img src="' + STATIC_URL + 'left_quotation_mark.svg" />');
        lq.width(32);
        lq.height(32);
        lq.css("position", "relative");
        lq.css("float", "left");
        var rq = $('<img src="' + STATIC_URL + 'right_quotation_mark.svg" />');
        rq.width(32);
        rq.height(32);
        rq.css("position", "relative");
        rq.css("float", "right");
        rq.css("top", "-32px");
        $(this).before(lq);
        $(this).after(rq);
    });

    $("p.content").keyup(function() {
        date = $(this).parent().children("h1").text();
        $.ajax({
            method: "POST",
            url: window.location.pathname,
            data: { content: $(this).text(), date: date }
        });
    });
});
