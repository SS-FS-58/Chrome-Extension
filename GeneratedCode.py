import os

# Export Directory
export_directory = "export"
# setting parameters
windows_width = 1000
windows_height = 800
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


class GenerateResizeExtension():
    def __init__(self, data):
        self.data = data
    # export all files for google chrome extension

    def generateExtension(self):
        print('Generating Resize Extension')
        self.generateManifestJson()
        self.generateBackgroundJs()
        self.generatePopup()
    # export manifest.json file

    def generateManifestJson(self):
        print('Generating manifest.json')
        # create
        file_name = self.data['export_dir'] + '/manifest.json'
        f = open(file_name, "w")
        # contents
        contents = """
{
  "name": "Resize windows",
  "version": "1.0",
  "description": "Test extension!",
  "background": {
    "scripts": [
      "background.js"
    ],
    "persistent": false
  },
  "browser_action": {
    "default_popup": "popup.html"
  },
  "manifest_version": 2
}
        """
        f.write(contents)
        f.close()
    # export background.js file

    def generateBackgroundJs(self):
        print('Generating background.js')
        # create
        file_name = self.data['export_dir'] + '/background.js'
        f = open(file_name, "w")
        # contents
        contents = """
chrome.runtime.onStartup.addListener(function () {
  chrome.windows.getCurrent(function (wind) {
    var updateInfo = {
      left: 0,
      top: 0,
      width: customWidth,
      height: customHeight,
    };
    chrome.windows.update(wind.id, updateInfo);
  });
});
        """
        # customize the width and height.
        contents = contents.replace(
            "customWidth", str(self.data['windows_width']))
        contents = contents.replace(
            "customHeight", str(self.data['windows_height']))
        f.write(contents)
        f.close()
    # export popup.html and popup.js files

    def generatePopup(self):
        print('Generating popup.html and popup.js')
        # 1. popup.html
        # create
        file_name = self.data['export_dir'] + '/popup.html'
        f = open(file_name, "w")
        # contents
        contents = """
<html>
  <head>
    <script src="popup.js"></script>
  </head>
  <body></body>
</html>
        """
        f.write(contents)
        f.close()
        # 2. popup.js
        # create
        file_name = self.data['export_dir'] + '/popup.js'
        f = open(file_name, "w")
        # contents
        contents = """
function Setting() {
  document.body.innerText = "Resize extension";
  chrome.windows.getCurrent(function (wind) {
    let updateInfo = {
      left: 0,
      top: 0,
      width: customWidth,
      height: customHeight,
    };
    chrome.windows.update(wind.id, updateInfo);
  });
}
window.onload = Setting;
        """
        # customize the width and height.
        contents = contents.replace(
            "customWidth", str(self.data['windows_width']))
        contents = contents.replace(
            "customHeight", str(self.data['windows_height']))
        f.write(contents)
        f.close()


def main():
    print('project started!')
    settingData = {
        'export_dir': export_directory,
        'windows_width': windows_width,
        'windows_height': windows_height
    }
    automation = GenerateResizeExtension(settingData)
    automation.generateExtension()


if __name__ == '__main__':
    main()
