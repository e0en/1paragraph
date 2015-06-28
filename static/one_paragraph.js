$("body").ready(function() {
    $(".content").each(function() {
        var lq = $('<img src="static/left_quotation_mark.svg" />');
        lq.width(32);
        lq.height(32);
        lq.css("position", "relative");
        lq.css("float", "left");
        var rq = $('<img src="static/right_quotation_mark.svg" />');
        rq.width(32);
        rq.height(32);
        rq.css("position", "relative");
        rq.css("float", "right");
        rq.css("top", "-32px");
        $(this).before(lq);
        $(this).after(rq);
    });
});
