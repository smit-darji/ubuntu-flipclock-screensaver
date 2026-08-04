import SwiftUI

struct ContentView: View {
    var body: some View {
        WebView(fileName: "index")
            .edgesIgnoringSafeArea(.all)
            .statusBar(hidden: true)
            .onAppear {
                // Keep screen awake while screensaver is active
                UIApplication.shared.isIdleTimerDisabled = true
            }
            .onDisappear {
                // Re-enable default sleep behavior on exit
                UIApplication.shared.isIdleTimerDisabled = false
            }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
