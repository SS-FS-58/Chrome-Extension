import os

# Export Directory
export_directory = "export"
# Path
c_path = os.getcwd()
print("The current working directory is %s" % c_path)
path = os.path.join(c_path, export_directory)
# Create a new directory.
try:
    os.mkdir(path)
except Exception as e:
    print(e)
    pass

print("Directory '% s' created" % export_directory)



def generateManifestJson(data):
    print('Generating manifest.json')
    # create
    file_name = export_directory + '/manifest.json'
    f = open(file_name, "w")
    # contents
    contents = """
{
  "name": "Resize windows",
  "version": "1.0",
  "description": "Test extension!",
  "browser_action": {
    "default_popup": "popup.html"
  },
  "manifest_version": 2
}
    """
    f.write(contents)
    f.close()

# export popup.html and popup.js files


def generatePopup(data):
    print('Generating popup.html and popup.js')
    # 1. popup.html
    # create
    file_name = export_directory + '/popup.html'
    f = open(file_name, "w")
    # contents
    contents = """
<html>
  <head>
    <script src="popup.js"></script>
  </head>
  <body>
    <div id="sizeTitle">Resize windows</div>
  </body>
</html>
    """
    f.write(contents)
    f.close()
    # 2. popup.js
    # create
    file_name = export_directory + '/popup.js'
    f = open(file_name, "w")
    # contents
    contents = """
var outerHeight, innerHeight, heightDelta;
chrome.windows.get(chrome.windows.WINDOW_ID_CURRENT, function (w) {
  outerHeight = w.height;
});

chrome.tabs.query({ active: true }, function (t) {
  innerHeight = t[0].height;
});

function Setting() {
  heightDelta = outerHeight - innerHeight;
  var w = Number(customWidth);
  var h = Number(customHeight);
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
    left: 0,
    top: 0,
    width: w,
    height: h,
  });
}
window.onload = Setting;

    """
    # customize the width and height.
    contents = contents.replace(
        "customWidth", str(data['windows_width']))
    contents = contents.replace(
        "customHeight", str(data['windows_height']))
    contents = contents.replace(
        "innerFlag", str(data['innerFlag']))
    f.write(contents)
    f.close()


def main():
    print('project started!')
    settingData = {
        'windows_width': 800,
        'windows_height': 700,
        'innerFlag': 'true'  # false or true
    }
    generateManifestJson(settingData)
    generatePopup(settingData)


if __name__ == '__main__':
    main()
