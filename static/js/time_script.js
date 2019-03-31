// Author: SA

// time function created which is called by layout.html
startTime();
function startTime() {
  var today = new Date();
  var h = today.getHours();
  var m = today.getMinutes();
  var s = today.getSeconds();
  // add a zero in front of numbers<10
  m = checkTime(m);
  s = checkTime(s);
  document.getElementById("clock").setText = h + ":" + m + ":" + s;
  var t = setTimeout(function() {
    startTime();
  }, 500);
}

function checkTime(i) {
  if (i < 10) {
    i = "0" + i; // add a zero in front of numbers<10
  }
  return i;
}

// var d = new Date();

// var utc_offset = d.getTimezoneOffset();
// d.setMinutes(d.getMinutes() + utc_offset);

// var ET_offset = -5+60;
// d.setMinutes(d.getMinutes() + ET_offset);

// function checkTime(i) {
// if (i < 10) {
// i = "0" + i
// }  // add zero in front of numbers < 10
// return i;

// }
