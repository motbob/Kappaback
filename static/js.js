var time = 0, z_time = 0;
var chat;
var chunkObj = {};
var offset = -28
function prependChatMsg(msg) {
	chatmsg = document.createElement("div");
	chatmsg.innerHTML = msg;
	chat.appendChild(chatmsg);
	chat.insertBefore(chatmsg, chat.firstChild);
};
function checkVideoTime() {
	try {
		z_time = Math.floor(ytplayer.getCurrentTime());
		if(z_time != time) {
			time = z_time;
			if(typeof msgs[time - offset] !== "undefined")
				prependChatMsg(msgs[time - offset]);
		}
	}
	catch(err) {
		//prependChatMsg(err);
	}
};
function onYouTubePlayerReady(playerId) {
	ytplayer = document.getElementById("myytplayer");
};
var msgs = {};
var flashvars = {};
var params = { scale: "exactFit", allowScriptAccess: "always" };
var atts = { id: "myytplayer" };
function httpGet(theUrl) {
	var xmlHttp;
	xmlHttp = new XMLHttpRequest();
	xmlHttp.onreadystatechange = function() {
		if (xmlHttp.readyState==4 && xmlHttp.status==200) {
			$.extend(msgs, JSON.parse(xmlHttp.responseText));
		}
	}
	xmlHttp.open( "GET", theUrl, true );
	xmlHttp.send( null );
};
