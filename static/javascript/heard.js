
$(document).ready(function() {

    /*
     We need to set a canary element to known dimensions in order to track the font size.  Creating an element for this purpose is antisocial as it alters the DOM in ways other scripts might not be expecting.  Unfortunately, the element has to be in the document's DOM, unattached elements don't work.

     The alternative is hijacking an existing element.  Most aren't suitable, but normally hidden elements such as SCRIPT and anything in HEAD are fairly safe.  Since we know for an almost-certain fact at least one script element exists (the one referring to jQuery), we'll use that.

     Some scripts use their own style properties as switches for behaviour, so to avoid interfering with them, we'll aim for the jQuery script element first (using the src attribute), and use another script element only if we can't find jQuery's.  As a last resort, a user can configure which element to use by setting the canary variable to either an element, a selector, or null (signifying that it's acceptable to create a dummy element).
     */
    var canary = "script[src*=jquery],script";

    if (typeof canary == "undefined" || canary == null) {
        canary = $(document.createElement("div"));
        $("body").append(canary.get(0));
    } else {
        canary = $(canary).eq(0);
    }
    canary.css({
        display: "block",
        width: "1em",
        height: "1em",
        margin: "0",
        padding: "0",
        position: "absolute",
        top: "-5em",
        left: "-5em",
        overflow: "hidden"
    });

    var currentFontSize = canary.width();
    window.setInterval(function() {
        var newFontSize = canary.width();
        if (currentFontSize != newFontSize) {
            $(window).triggerHandler("fontResize", [newFontSize, currentFontSize]);
            currentFontSize = newFontSize;
        }
    }, 200);

    var newcomer = $("#newcomer");

    var cancel = newcomer.find("button.cancel")
    cancel.addClass("text");
    cancel.text("x");

    var offset = newcomer.offset();
    cancel.css({
        position: "absolute",
        top: offset.top + "px",
        left: (offset.left + newcomer.width()) + "px",
        marginTop: "0.25em",
        marginLeft: "-1.5em"
    });

    cancel.click(function(event) {
        newcomer.fadeOut("slow");
        return false;
    });

    newcomer.find("form").submit(function() {

        var heard = newcomer.find("input[name=heard]");
        if (heard.val() == "") {
            var instructions = newcomer.find("h2 + p");

            /*
             * Replacement text can make the content below it jump if it takes up more space.
             * Since we know the replacement text is shorter, we can solve this by set the height explicitly to its original computed value.
             */
            instructions.css("height", instructions.height() + "px");

            /*
             * However, this causes a secondary problem if the font is resized afterwards.
             * To remedy this, we take away the explicitly set height if the font is resized.
             * Since the page is being redrawn anyway, the jumping doesn't matter.
             */
            $(window).one("fontResize.heard", function(event, newSize, oldSize) {
                instructions.css("height", "auto");
            });

            instructions.fadeOut("slow", function() {
                instructions.text("Don't forget to type something!");
                instructions.fadeIn("slow", function() {
                    heard.get(0).focus();
                });
            });
            heard.get(0).blur();
            return false;
        }
        var paragraph = newcomer.find("p");
        newcomer.find("p,form").fadeOut("slow", function() {
            paragraph.text("Thanks for the feedback!");
            paragraph.fadeIn("slow", function() {
                window.setTimeout(function() {
                    newcomer.fadeOut("slow");
                }, 2500);
            });
        });
        return false;
    });
});

