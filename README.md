# 🛡️ AI Moderation Service

Dịch vụ AI kiểm duyệt nội dung (hate speech detection) cho ứng dụng web Java Servlet.  
Sử dụng **PhoBERT** fine-tuned trên dữ liệu tiếng Việt.

## 📁 Cấu trúc project

```
ai-moderation-service/
│
├── app.py                 # ⭐ API chính (FastAPI)
├── requirements.txt       # Thư viện cần cài
│
├── model/                 # ⭐ Model đã train
│   └── phobert-hate-speech-final_V2/
│       ├── config.json
│       ├── model.safetensors
│       ├── tokenizer_config.json
│       ├── vocab.txt
│       ├── bpe.codes
│       └── added_tokens.json
│
├── utils/                 # Helper modules
│   └── predict.py         # Logic phân loại
│
└── README.md
```

## 🚀 Cài đặt & Chạy

### 1. Tạo virtual environment (khuyến khích)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 2. Cài thư viện

```bash
pip install -r requirements.txt
```

### 3. Chạy server

```bash
python app.py
```

Hoặc:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Server sẽ chạy tại: **http://localhost:8000**

## 📖 API Endpoints

### Health Check

```
GET /
GET /health
```

### Kiểm duyệt đơn lẻ

```
POST /api/moderate
Content-Type: application/json

{
    "text": "nội dung cần kiểm duyệt"
}
```

**Response:**

```json
{
    "label": "CLEAN",
    "label_id": 0,
    "confidence": 0.9876,
    "probabilities": {
        "CLEAN": 0.9876,
        "OFFENSIVE": 0.0089,
        "HATE": 0.0035
    },
    "is_toxic": false
}
```

### Kiểm duyệt hàng loạt (batch)

```
POST /api/moderate/batch
Content-Type: application/json

{
    "texts": [
        "xin chào mọi người",
        "nội dung khác cần kiểm tra"
    ]
}
```

**Response:**

```json
{
    "results": [
        {
            "label": "CLEAN",
            "label_id": 0,
            "confidence": 0.9912,
            "probabilities": { "CLEAN": 0.9912, "OFFENSIVE": 0.0055, "HATE": 0.0033 },
            "is_toxic": false
        }
    ],
    "total": 2,
    "toxic_count": 0
}
```

## 🔗 Gọi từ Java Servlet

```java
import java.io.*;
import java.net.*;
import org.json.*;

public class ModerationHelper {

    private static final String AI_URL = "http://localhost:8000/api/moderate";

    /**
     * Gọi AI service để kiểm duyệt nội dung.
     * @param text Nội dung cần kiểm duyệt
     * @return true nếu nội dung vi phạm (OFFENSIVE hoặc HATE)
     */
    public static boolean isToxic(String text) throws Exception {
        URL url = new URL(AI_URL);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("POST");
        conn.setRequestProperty("Content-Type", "application/json; charset=UTF-8");
        conn.setDoOutput(true);

        // Gửi request
        String jsonBody = "{\"text\": \"" + escapeJson(text) + "\"}";
        try (OutputStream os = conn.getOutputStream()) {
            os.write(jsonBody.getBytes("UTF-8"));
        }

        // Đọc response
        StringBuilder response = new StringBuilder();
        try (BufferedReader br = new BufferedReader(
                new InputStreamReader(conn.getInputStream(), "UTF-8"))) {
            String line;
            while ((line = br.readLine()) != null) {
                response.append(line);
            }
        }

        // Parse JSON
        JSONObject json = new JSONObject(response.toString());
        return json.getBoolean("is_toxic");
    }

    private static String escapeJson(String text) {
        return text.replace("\\", "\\\\")
                   .replace("\"", "\\\"")
                   .replace("\n", "\\n")
                   .replace("\r", "\\r");
    }
}
```

**Sử dụng trong Servlet:**

```java
@WebServlet("/post")
public class PostServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {

        String content = req.getParameter("content");

        try {
            if (ModerationHelper.isToxic(content)) {
                // ❌ Nội dung vi phạm → từ chối
                req.setAttribute("error", "Nội dung chứa ngôn ngữ không phù hợp!");
                req.getRequestDispatcher("/post-form.jsp").forward(req, resp);
                return;
            }
        } catch (Exception e) {
            // AI service lỗi → cho qua (hoặc xử lý tùy ý)
            e.printStackTrace();
        }

        // ✅ Nội dung OK → lưu bài viết bình thường
        // postDAO.save(...)
    }
}
```

## 📊 Labels

| Label ID | Label       | Ý nghĩa                        |
|----------|-------------|----------------------------------|
| 0        | CLEAN       | Bình thường, không vi phạm      |
| 1        | OFFENSIVE   | Ngôn ngữ xúc phạm              |
| 2        | HATE        | Phát ngôn thù ghét (hate speech)|

## 📌 Lưu ý

- Server AI cần **chạy trước** khi khởi động Java web app.
- Port mặc định: **8000** (có thể đổi trong `app.py`).
- Lần đầu khởi động sẽ mất vài giây để load model vào RAM.
- Model dung lượng ~540MB, cần đủ RAM (tối thiểu 2GB free).
