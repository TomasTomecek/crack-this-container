jQuery(document).ready(function($) {
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
        $("#winners").append('<li>' + msg + '</li>');
    }
});
