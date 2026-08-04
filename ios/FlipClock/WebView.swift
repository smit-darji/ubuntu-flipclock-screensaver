import SwiftUI
import WebKit

struct WebView: UIViewRepresentable {
    let fileName: String

    func makeUIView(context: Context) -> WKWebView {
        let configuration = WKWebViewConfiguration()
        
        // Enable local file and database storage capabilities
        configuration.preferences.setValue(true, forKey: "allowFileAccessFromFileURLs")
        configuration.preferences.setValue(true, forKey: "allowUniversalAccessFromFileURLs")
        
        let webView = WKWebView(frame: .zero, configuration: configuration)
        webView.navigationDelegate = context.coordinator
        
        // Prevent accidental swiping or scrolling
        webView.scrollView.isScrollEnabled = false
        webView.scrollView.bounces = false
        
        #if DEBUG
        if #available(iOS 16.4, *) {
            webView.isInspectable = true // Enable Safari remote debugger
        }
        #endif

        return webView
    }

    func updateUIView(_ uiView: WKWebView, context: Context) {
        guard let path = Bundle.main.path(forResource: fileName, ofType: "html") else {
            print("Error: Resource \(fileName).html not found in main bundle")
            return
        }
        
        let fileURL = URL(fileURLWithPath: path)
        let directoryURL = fileURL.deletingLastPathComponent()
        
        // Load the file granting read access to its directory folder
        uiView.loadFileURL(fileURL, allowingReadAccessTo: directoryURL)
    }

    func makeCoordinator() -> Coordinator {
        Coordinator()
    }

    class Coordinator: NSObject, WKNavigationDelegate {
        // WKNavigationDelegate handlers if needed
    }
}
