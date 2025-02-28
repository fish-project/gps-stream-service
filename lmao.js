// Địa chỉ WebSocket server
        const ws_url = "ws://localhost:8010/stream/ship_test_gps";
        
        // Tạo kết nối WebSocket
        const ws = new WebSocket(ws_url);

        // Khi kết nối WebSocket mở
        ws.onopen = function() {
            const statusElement = document.getElementById('status');
            if (statusElement) {
                statusElement.innerText = "Connected to WebSocket server";
            }

            // Gửi dữ liệu mỗi 2 giây
            setInterval(function() {
                const data = {
                    latitude: (Math.random() * (90 - (-90)) + (-90)).toFixed(6),  // Tọa độ vĩ độ ngẫu nhiên
                    longitude: (Math.random() * (180 - (-180)) + (-180)).toFixed(6)  // Tọa độ kinh độ ngẫu nhiên
                };
                ws.send(JSON.stringify(data));
                console.log("Sent:", data);
            }, 2000);
        };

        // Nhận dữ liệu từ WebSocket server
        ws.onmessage = function(event) {
            const message = event.data;
            const messagesElement = document.getElementById('messages');
            if (messagesElement) {
                messagesElement.innerText = "Received: " + message;
            }
            console.log("Received:", message);
        };

        // Xử lý lỗi WebSocket
        ws.onerror = function(error) {
            console.error("WebSocket error:", error);
            const statusElement = document.getElementById('status');
            if (statusElement) {
                statusElement.innerText = "Error connecting to WebSocket server";
            }
        };

        // Khi kết nối WebSocket đóng
        ws.onclose = function(event) {
            const statusElement = document.getElementById('status');
            if (statusElement) {
                statusElement.innerText = "Disconnected from WebSocket server";
            }
            console.log("Disconnected from WebSocket server:", event);
        };