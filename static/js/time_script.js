function startTime() {
    var day = new Date();
    var h = day.getHours();
    var m = day.getMinutes();
    var s = day.getSeconds();
    m = checkTime(m);
    s = checkTime(s);
    document.getElementById('txt').innerHTML = h + ":" + m + ":" + s;
    var t = setTimeout(startTime, 500);
  }

  function checkTime(i) {
    if (i < 10) {
        i = "0" + i
    }  // add zero in front of numbers < 10
    return i;
  }
