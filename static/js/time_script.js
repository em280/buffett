// Author: SA

// time function created which is called by layout.html
startTime();

function startTime() {
  var day = new Date();
  var h = day.getHours();
  var m = day.getMinutes();
  var s = day.getSeconds();
  m = checkTime(m);
  s = checkTime(s);
  document.querySelector("#clock").innerHTML = h + ":" + m + ":" + s;
  var t = setTimeout(startTime, 500);

  function checkTime(i) {
    if (i < 10) {
      i = "0" + i;
    } // add zero in front of numbers < 10
    return i;
  }
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
