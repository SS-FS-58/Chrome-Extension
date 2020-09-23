
var outerHeight, innerHeight, heightDelta;
chrome.windows.get(chrome.windows.WINDOW_ID_CURRENT, function (w) {
  outerHeight = w.height;
});

chrome.tabs.query({ active: true }, function (t) {
  innerHeight = t[0].height;
});

function Setting() {
  heightDelta = outerHeight - innerHeight;
  var w = Number(1500);
  var h = Number(800);
  if (800) {
    h += heightDelta;
  }
  let tooltipTxt = (800 ? "InnerSize:" : "OuterSize:").concat(
    1500,
    "*",
    800,
    " "
  );
  document.getElementById("sizeTitle").innerHTML = tooltipTxt;
  chrome.windows.update(chrome.windows.WINDOW_ID_CURRENT, {
    left: 0,
    top: 0,
    width: w,
    height: h,
  });
}
window.onload = Setting;

    