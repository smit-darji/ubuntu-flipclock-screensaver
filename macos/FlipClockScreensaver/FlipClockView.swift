import ScreenSaver
import WebKit

class FlipClockView: ScreenSaverView {
    private var webView: WKWebView?

    override init?(frame: NSRect, isPreview: Bool) {
        super.init(frame: frame, isPreview: isPreview)
        setupWebView()
    }

    required init?(coder: NSCoder) {
        super.init(coder: coder)
        setupWebView()
    }

    private func setupWebView() {
        let configuration = WKWebViewConfiguration()
        
        // Grant permissions for local files and database storage
        configuration.preferences.setValue(true, forKey: "allowFileAccessFromFileURLs")
        configuration.preferences.setValue(true, forKey: "allowUniversalAccessFromFileURLs")
        
        let webView = WKWebView(frame: bounds, configuration: configuration)
        webView.autoresizingMask = [.width, .height]
        
        // Prevent scrollbars and bounces
        webView.scrollView.isScrollEnabled = false
        webView.scrollView.bounces = false
        
        addSubview(webView)
        self.webView = webView
        
        loadClockHTML()
    }

    private func loadClockHTML() {
        guard let webView = webView else { return }
        
        // Find index.html inside the screensaver .saver bundle
        let bundle = Bundle(for: type(of: self))
        guard let path = bundle.path(forResource: "index", ofType: "html") else {
            print("Error: index.html not found in screensaver bundle.")
            return
        }
        
        let fileURL = URL(fileURLWithPath: path)
        let directoryURL = fileURL.deletingLastPathComponent()
        
        // Load local file with directory read permissions
        webView.loadFileURL(fileURL, allowingReadAccessTo: directoryURL)
    }

    override func startAnimation() {
        super.startAnimation()
    }

    override func stopAnimation() {
        super.stopAnimation()
    }

    override func animateOneFrame() {
        // Redraw triggers automatically via HTML/JS, no animation CPU draw needed.
    }

    override var hasConfigureSheet: Bool {
        return false // Double-click inside screensaver opens web-based settings
    }

    override var configureSheet: NSWindow? {
        return nil
    }
}
