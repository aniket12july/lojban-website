
soundManager.debugMode = false;
soundManager.defaultOptions.multiShot = false;
soundManager.defaultOptions.allowPolling = false;
soundManager.createMovie("/javascript/audio/soundmanager2.swf");

$(document).ready(function(){

    /* Disable the play links because they won't work until SoundManager2 has loaded. */
    $("#word-of-the-day .example a").click(function() {
        this.blur();
        return false;
    });

    soundManager.onload = function() {

        /* Initialise each audio file. */
        $("#word-of-the-day .example a[type=audio/mp3]").each(function() {
            soundManager.createSound({
                id: this.href,
                url: this.href
            });
            $(this).find("img").attr("src", "/images/play-enabled.png");
        });

        /* Remove the event handler that disabled the play links. */
        $("#word-of-the-day .example a").unbind();

        $("#word-of-the-day .example a").click(function() {
            this.blur();
            if (this.playing) return false;
            this.playing = true;

            var img = $(this).find("img");
            img.attr("src", "/images/play-disabled.png");
            soundManager.play(this.href, {
                onfinish: function() {
                    img.attr("src", "/images/play-enabled.png");
                    img.get(0).parentNode.focus();
                    img.get(0).parentNode.playing = false;
                }
            });
            if (soundManager.getSoundById(this.href).readyState == 2) {
                img.attr("src", "/images/error.png");
                img.attr("title", "This sound file is not available.");
            }
            return false;
        });

    }

    soundManager.onerror = function() {
        /* Something's gone wrong with SoundManager2, so fall back to browser's native support. */

        /* Remove the event handler that disabled the play links. */
        $("#word-of-the-day .example a").unbind();

        $("#word-of-the-day .example a[type=audio/mp3] img").attr("src", "/images/play-enabled.png");
    };

});
