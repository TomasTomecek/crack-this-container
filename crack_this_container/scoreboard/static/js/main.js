$(function() {
    var ws4redis = WS4Redis({
        uri: url('solution-submitted'),
        connecting: on_connecting,
        connected: on_connected,
        receive_message: receiveMessage,
        disconnected: on_disconnected,
        heartbeat_message: "X"
    });

    function url(s) {
        var l = window.location;
        return ((l.protocol === "https:") ? "wss://" : "ws://") + l.host + "/ws/" + s +
          "?subscribe-broadcast&publish-broadcast";  // &echo
    }

    function on_connecting() {
        console.log('Websocket is connecting...');
    }

    function on_connected() {
        console.log('connected');
        // ws4redis.send_message('Hello');
    }

    function on_disconnected(evt) {
        console.log('Websocket was disconnected: ' + JSON.stringify(evt));
    }

    // receive a message though the websocket from the server
    function receiveMessage(msg) {
        console.log(msg);
        if (msg !== "TOO_LATE") {
          var displayed_entries=$("#winners li button").text();
          if (displayed_entries.indexOf(msg) === -1) {
            var b=$("#hidden-winner-button").clone();
            var h=b.html().replace("TEXT", msg);
            $("ul#winners").append("<li>" + h + "</li>");
          }
        }
        $('#solved-count').html(function(i, oldval) {
          return ++oldval;
        });
    }

    // stopwatch
    var stopwatch;

    function start_stopwatch() {
    }

    function tick() {
      stopwatch.add(1, "second");
      var t=stopwatch.format('mm : ss');
      $("#timer").html(t);
      t = setTimeout(function () {
        tick();
      }, 1000);
    }

    var timer_div=$("#timer");
    if (timer_div.length > 0) {
      stopwatch=moment(timer_div.html(), ["mm : ss"]);
      tick();
    }

    $("#game-control button").click(function() {
      $.post(
        "/api/v0/game/latest/start/",
        {},
        function(data) {
          if (stopwatch === undefined) {
            $("#game-control").html("<div id=\"timer\"></div>");
            stopwatch="00 : 00";
            tick();
          }
        },
        'json'
      );
    });
});
