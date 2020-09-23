var outerHeight, innerHeight, heightDelta;
chrome.windows.get(chrome.windows.WINDOW_ID_CURRENT, function (w) {
  outerHeight = w.height;
});

chrome.tabs.query({ active: true }, function (t) {
  innerHeight = t[0].height;
});

function Setting() {
  heightDelta = outerHeight - innerHeight;
  const customWidth = "1000";
  const customHeight = "800";
  var w = Number(customWidth);
  var h = Number(customHeight);
  const innerFlag = true;
  if (innerFlag) {
    h += heightDelta;
  }
  let tooltipTxt = (innerFlag ? "InnerSize:" : "OuterSize:").concat(
    customWidth,
    "*",
    customHeight,
    " "
  );
  document.getElementById("sizeTitle").innerHTML = tooltipTxt;
  chrome.windows.update(chrome.windows.WINDOW_ID_CURRENT, {
    width: w,
    height: h,
  });
}
window.onload = Setting;
