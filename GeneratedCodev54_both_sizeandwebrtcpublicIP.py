import os

# Export Directory
export_directory = "extension_both_sizeandwebrtcpublicIP"
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
  "manifest_version": 2,
  "name": "Size and WebrtcpublicIP",
  "version": "1.1.0",
  "content_scripts": [
    {
      "matches": ["<all_urls>"],
      "js": ["content-script.js"],
      "run_at": "document_start"
    }
  ],
  "permissions": [
    "<all_urls>",
    "webRequest",
    "webRequestBlocking"
    ]
}

    """
    f.write(contents)
    f.close()

# export popup.html and popup.js files


def generateContentScript(data):
    print('Generating content-script.js')
    # create content-script.js
    file_name = export_directory + '/content-script.js'
    f = open(file_name, "w")
    # contents
    contents = """
    
// Breaks out of the content script context by injecting a specially
// constructed script tag and injecting it into the page.
// See: https://intoli.com/blog/sandbox-breakout/
const runInPageContext = (method, ...args) => {
  // The stringified method which will be parsed as a function object.
  const stringifiedMethod = method instanceof Function
    ? method.toString()
    : `() => { ${method} }`;

  // The stringified arguments for the method as JS code that will reconstruct the array.
  const stringifiedArgs = JSON.stringify(args);

  // The full content of the script tag.
  const scriptContent = `
    // Parse and run the method with its arguments.
    (${stringifiedMethod})(...${stringifiedArgs});

    // Remove the script element to cover our tracks.
    document.currentScript.parentElement
      .removeChild(document.currentScript);
  `;

  // Create a script tag and inject it into the document.
  const scriptElement = document.createElement('script');
  scriptElement.innerHTML = scriptContent;
  document.documentElement.prepend(scriptElement);
};


// Applies a random browser fingerprint within a page context.
// See: https://intoli.com/blog/not-possible-to-block-chrome-headless/
const applyBrowserFingerprintFromUserAgents = (browserFingerprint) => {
  // Pass the Webdriver Test.
  Object.defineProperty(navigator, 'webdriver', {
    get: () => {
      if (/firefox/i.test(browserFingerprint.userAgent)) {
        return false;
      }
      return undefined;
    },
  });

  // Pass the Chrome Test.
  // We can mock this in as much depth as we need for the test.
  window.chrome = {
    runtime: {},
    // etc.
  };

  // Pass the Permissions Test.
  const originalQuery = window.navigator.permissions.query;
  window.navigator.permissions.query = parameters => (
    parameters.name === 'notifications' ?
      Promise.resolve({ state: Notification.permission }) :
      originalQuery(parameters)
  );

  // Pass the Plugins Length Test.
  // Overwrite the `plugins` property to use a custom getter.
  Object.defineProperty(navigator, 'plugins', {
    // This just needs to have `length > 0` for the current test,
    // but we could mock the plugins too if necessary.
    get: () => Array(browserFingerprint.pluginsLength).fill(),
  });

  // Pass the Languages Test.
  Object.defineProperty(navigator, 'languages', {
    get: () => [browserFingerprint.language || 'en-US'],
  });

  // Attach the remaining navigator properties.
  const navigatorProperties = [
    'appName',
    'connection',
    'cpuClass',
    'language',
    'oscpu',
    'platform',
    'userAgent',
    'vendor',
  ];
  navigatorProperties
    .map(key => [key, browserFingerprint[key]])
    .filter(([, value]) => value !== undefined)
    .forEach(([key, value]) => {
      // Overwrite the `key` property to use a custom getter.
      Object.defineProperty(navigator, key, {
        get: () => value,
      });
    });
};



// A variation of the above which handles the more extensive format from tracking pixels.
const applyBrowserSize = (browserFingerprint) => {
  window.innerHeight = browserFingerprint.innerHeight;
  window.innerWidth = browserFingerprint.innerWidth;
  Object.defineProperty(window.screen, 'height', { get: () => browserFingerprint.screen_height });
  Object.defineProperty(window.screen, 'width', { get: () => browserFingerprint.screen_width });

  Object.defineProperty(RTCIceCandidate.prototype, 'candidate', {
    get: function () {
      try {
        const originalCandidate = RTCIceCandidateCandidateGetter.apply(this);
        const ipRegex = /([0-9]{1,3}(\.[0-9]{1,3}){3}|[a-f0-9]{1,4}(:[a-f0-9]{1,4}){7})/;
        return originalCandidate.replace(ipRegex, browserFingerprint.webrtc_localIP);
      } catch (error) {
        return null;
      }
    },
  });
  Object.defineProperty(RTCPeerConnection.prototype, 'localDescription', {
    get: function () {
        return {
            sdp: ''
        }
    }
  })
  
};

// Parse the stringified browser fingerprint.
// This value is filled in from Python as a template variable.
const browserFingerprint = JSON.parse("{\\"screen_width\\" : customScreenWidth, \\"screen_height\\" : customScreenHeight, \\"innerWidth\\" : customInnerWidth, \\"innerHeight\\" : customInnerHeight, \\"webrtc_publicIP\\" : customWebrtcPublicIP}");
// Apply the overrides in the context of the page.
if (/user_agents/i.test(browserFingerprint.fingerprintType)) {
  runInPageContext(applyBrowserFingerprintFromUserAgents, browserFingerprint);
} else {
  runInPageContext(applyBrowserSize, browserFingerprint);
}

    """
    # customize the width and height.
    contents = contents.replace(
        "customScreenWidth", str(data['screen_width']))
    contents = contents.replace(
        "customScreenHeight", str(data['screen_height']))
    contents = contents.replace(
        "customInnerWidth", str(data['inner_width']))
    contents = contents.replace(
        "customInnerHeight", str(data['inner_height']))
    contents = contents.replace(
        "customWebrtcPublicIP", str(data['webrtc_publicIP']))
    f.write(contents)
    f.close()

def main():
    print('project started!')
    settingData = {
        'screen_width': 1920,
        'screen_height': 1080,
        'inner_width': 1519,
        'inner_height': 754,
        'webrtc_publicIP': "null"
    }
    generateManifestJson(settingData)
    generateContentScript(settingData)

if __name__ == '__main__':
    main()
