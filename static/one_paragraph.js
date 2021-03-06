$("body").ready(function() {
    var qSize = 24;
    $(".content").each(function() {
        var lq = $('<img src="' + STATIC_URL + 'left_quotation_mark.svg" />');
        lq.width(qSize);
        lq.height(qSize);
        lq.css("position", "relative");
        lq.css("float", "left");
        var rq = $('<img src="' + STATIC_URL + 'right_quotation_mark.svg" />');
        rq.width(qSize);
        rq.height(qSize);
        rq.css("position", "relative");
        rq.css("float", "right");
        rq.css("top", "-32px");
        $(this).before(lq);
        $(this).after(rq);
    });

    $("p.content").focus();

    $("h1").focusout(function() {
        date = $(this).text();
        window.location.replace("/diary/" + date);
    });

    $("h1").keypress(function(e) {
        if (e.which == 13) {
            event.preventDefault();
            date = $(this).text();
            window.location.replace("/diary/" + date);
       }
    });

    $("p.content").keyup(function() {
        date = $(this).parent().children("h1").text();
        $.ajax({
            method: "POST",
            url: window.location.pathname,
            data: { content: $(this).text(), date: date }
        });
    });
    $("p.content").keypress(function(e) {
        if (e.which == 13) {
            event.preventDefault();
            date = $(this).parent().children("h1").text();
            $.ajax({
                method: "POST",
                url: window.location.pathname,
                data: { content: $(this).text(), date: date }
            });
        }
    });
});
