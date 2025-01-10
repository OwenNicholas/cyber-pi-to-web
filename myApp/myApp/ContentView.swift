import SwiftUI

struct ContentView: View {
    @State private var urlText: String = "http://" // Default URL for ON/OFF
    @State private var responseText: String = "Enter a URL and press ON / OFF Button"
    @State private var titleText: String = "ESP32 Outputs Controller"
    @State private var urlText2: String = "" // Default URL for GET
    @State private var getResponseText: String = "Enter a URL for GET and press GET Button"

    var body: some View {
        VStack(spacing: 20) {
            // Title
            Text(titleText)
                .font(.system(size: 20, weight: .heavy, design: .default))
            
            // TextField for ON/OFF URL input
            TextField("Enter URL", text: $urlText)
                .textFieldStyle(RoundedBorderTextFieldStyle())
                .padding()
            
            // HStack for ON/OFF Buttons
            HStack(spacing: 20) {
                // On Button: Turn on LED
                Button(action: {
                    fetchPostOn(from: urlText)
                }) {
                    Label("ON", systemImage: "power.circle.fill")
                }
                .buttonStyle(.borderedProminent)
                
                // Off Button: Turn off LED
                Button(action: {
                    fetchPostOff(from: urlText)
                }) {
                    Label("OFF", systemImage: "power.circle")
                }
                .buttonStyle(.bordered)
            }
            
            // Display the fetched response for ON/OFF
            ScrollView {
                Text(responseText)
                    .padding()
                    .multilineTextAlignment(.center)
            }
            .frame(maxHeight: 50) // Limit scrollable area height
            
            // TextField for GET request URL
            TextField("Enter URL for GET", text: $urlText2)
                .textFieldStyle(RoundedBorderTextFieldStyle())
                .padding()
            
            // GET Button
            Button(action: {
                fetchPostGet(from: urlText2)
            }) {
                Label("GET", systemImage: "globe")
            }
            .buttonStyle(.borderedProminent)
            
            // Display the fetched response for GET
            ScrollView {
                Text(getResponseText)
                    .padding()
                    .multilineTextAlignment(.center)
            }
            .frame(maxHeight: 100) // Limit scrollable area height
        }
        .padding()
    }
    
    // ON Button Function
    private func fetchPostOn(from urlString: String) {
        let fullURLString = urlString.hasSuffix("/") ? urlString + "led1ON" : urlString + "/led1ON"
        
        guard let url = URL(string: fullURLString) else {
            responseText = "Invalid URL"
            return
        }
        
        URLSession.shared.dataTask(with: url) { data, response, error in
            if let error = error {
                DispatchQueue.main.async {
                    responseText = "Error: \(error.localizedDescription)"
                }
                return
            }
            
            guard let data = data else {
                DispatchQueue.main.async {
                    responseText = "No data received"
                }
                return
            }
            
            do {
                if let json = try JSONSerialization.jsonObject(with: data, options: []) as? [String: Any] {
                    DispatchQueue.main.async {
                        responseText = ""
                    }
                } else {
                    DispatchQueue.main.async {
                        responseText = "Failed to parse JSON"
                    }
                }
            } catch {
                DispatchQueue.main.async {
                    responseText = "Decoding error: \(error.localizedDescription)"
                }
            }
        }.resume()
    }
    
    // OFF Button Function
    private func fetchPostOff(from urlString: String) {
        let fullURLString = urlString.hasSuffix("/") ? urlString + "led1OFF" : urlString + "/led1OFF"
        
        guard let url = URL(string: fullURLString) else {
            responseText = "Invalid URL"
            return
        }
        
        URLSession.shared.dataTask(with: url) { data, response, error in
            if let error = error {
                DispatchQueue.main.async {
                    responseText = "Error: \(error.localizedDescription)"
                }
                return
            }
            
            guard let data = data else {
                DispatchQueue.main.async {
                    responseText = "No data received"
                }
                return
            }
            
            do {
                if let json = try JSONSerialization.jsonObject(with: data, options: []) as? [String: Any] {
                    DispatchQueue.main.async {
                        responseText = ""
                    }
                } else {
                    DispatchQueue.main.async {
                        responseText = "Failed to parse JSON"
                    }
                }
            } catch {
                DispatchQueue.main.async {
                    responseText = "Decoding error: \(error.localizedDescription)"
                }
            }
        }.resume()
    }
    
    // GET Button Function
    private func fetchPostGet(from urlString: String) {
        let fullURLString = urlText + urlText2
        
        guard let url = URL(string: fullURLString) else {
            getResponseText = "Invalid URL"
            return
        }
        
        URLSession.shared.dataTask(with: url) { data, response, error in
            if let error = error {
                DispatchQueue.main.async {
                    getResponseText = "Error: \(error.localizedDescription)"
                }
                return
            }
            
            guard let data = data else {
                DispatchQueue.main.async {
                    getResponseText = "No data received"
                }
                return
            }
            
            do {
                if let json = try JSONSerialization.jsonObject(with: data, options: []) as? [String: Any] {
                    DispatchQueue.main.async {
                        getResponseText = "Fetched Data:\n\(json.description)"
                    }
                } else {
                    DispatchQueue.main.async {
                        getResponseText = "Failed to parse JSON"
                    }
                }
            } catch {
                DispatchQueue.main.async {
                    getResponseText = "Decoding error: \(error.localizedDescription)"
                }
            }
        }.resume()
    }
}

#Preview {
    ContentView()
}
