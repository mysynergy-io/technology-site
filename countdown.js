(function () {
  // Target: 21 June 2026, 12:00 HKT/SGT (UTC+8)
  // ISO with explicit +08:00 offset so it doesn't drift on visitors in other zones.
  var TARGET = new Date('2026-06-21T12:00:00+08:00').getTime();

  var elDays   = document.getElementById('cd-days');
  var elHours  = document.getElementById('cd-hours');
  var elMins   = document.getElementById('cd-mins');
  var elSecs   = document.getElementById('cd-secs');

  function pad(n, w) { n = String(n); while (n.length < w) n = '0' + n; return n; }

  function tick() {
    var now = Date.now();
    var diff = TARGET - now;
    if (diff <= 0) {
      elDays.textContent  = '00';
      elHours.textContent = '00';
      elMins.textContent  = '00';
      elSecs.textContent  = '00';
      return;
    }
    var s = Math.floor(diff / 1000);
    var d = Math.floor(s / 86400); s -= d * 86400;
    var h = Math.floor(s / 3600);  s -= h * 3600;
    var m = Math.floor(s / 60);    s -= m * 60;
    elDays.textContent  = pad(d, 3);
    elHours.textContent = pad(h, 2);
    elMins.textContent  = pad(m, 2);
    elSecs.textContent  = pad(s, 2);
  }

  tick();
  setInterval(tick, 1000);

  // Apply-button gate — hidden entirely until launch time, then revealed.
  var btn = document.getElementById('cl-apply');
  if (btn) {
    var launchAt = new Date(btn.getAttribute('data-launch-at')).getTime();
    function refreshApply() {
      if (Date.now() < launchAt) {
        btn.setAttribute('hidden', '');
      } else {
        btn.removeAttribute('hidden');
      }
    }
    refreshApply();
    setInterval(refreshApply, 30000);
  }
})();
