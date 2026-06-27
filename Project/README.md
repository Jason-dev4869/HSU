# Multilingual Named Entity Recognition (mNER) Demo

Một hệ thống nhận diện thực thể đa ngôn ngữ (PER / LOC / ORG), gồm phần
huấn luyện model (fine-tune XLM-RoBERTa trên WikiANN), backend phục vụ
model qua API, và giao diện web HTML/CSS/JS để demo trực tiếp.

---

## 1. Cấu trúc project

```
.
├── doc/
│   ├── 1911.02116v2.pdf          # paper XLM-RoBERTa (Conneau et al.)
│   ├── Chapter4_mNER.pdf
│   └── NLP_Project_25.2A.pdf
├── interface/
│   ├── backend.py                  # FastAPI server phục vụ model
│   ├── index.html                  # giao diện web demo
│   ├── script.js                    # logic gọi API + render kết quả
│   └── style.css                     # style (Bootstrap + override màu riêng)
├── mner-production/                # model chính thức sau khi train
├── train.py                            # script huấn luyện model
├── requirements.txt              # danh sách thư viện cần cài
├── Training Log.txt                # log quá trình train (qua tee/redirect)
└── README.md
```

---

## 2. Cài đặt

### Yêu cầu

* Python 3.9+
* Có GPU NVIDIA (khuyến nghị, không bắt buộc — train trên CPU vẫn chạy được nhưng chậm hơn nhiều)

### Bước cài

```bash
pip install -r requirements.txt --break-system-packages
```

Nếu máy có GPU NVIDIA, nên cài `torch` bản CUDA riêng trước (lấy đúng lệnh
theo cấu hình máy tại https://pytorch.org/get-started/locally/), sau đó mới
chạy lệnh trên cho các thư viện còn lại — bản `torch` mặc định trên PyPI
không phải lúc nào cũng đi kèm đúng bản CUDA của máy.

Kiểm tra GPU có được nhận không:

```bash
python -c "import torch; print(torch.cuda.is_available())"
```

---

## 3. Cách sử dụng

### Bước 1 — Huấn luyện model

```bash
python train_mner_wikiann.py
```

Script sẽ tự tải dữ liệu WikiANN cho các ngôn ngữ đã chọn, fine-tune
XLM-RoBERTa, đánh giá trên test set, rồi lưu model chính thức vào
`./mner-production`. Các checkpoint tạm trong lúc train sẽ tự bị xóa sau
khi model chính thức được lưu xong — chỉ còn lại đúng một bản model cuối
trên đĩa.

Có thể chỉnh các biến ở đầu file để phù hợp với thời gian/phần cứng:

* `LANGUAGES`: danh sách ngôn ngữ lấy từ WikiANN
* `MAX_TRAIN_PER_LANG`: giới hạn số câu train mỗi ngôn ngữ (giảm để train nhanh hơn)
* `num_train_epochs`: số epoch tối đa (có `EarlyStoppingCallback` tự dừng sớm nếu không cải thiện)

### Bước 2 — Chạy backend

```bash
uvicorn backend:app --reload --port 8000
```

Backend load model từ `./mner-production` và mở endpoint `POST /predict`
nhận `{ "text": "..." }`, trả về danh sách thực thể tìm được.

### Bước 3 — Mở giao diện web

Mở `index.html` bằng Live Server (VS Code) hoặc double-click mở trực tiếp
bằng browser. Trang sẽ gọi tới `http://localhost:8000/predict`, nên backend
ở bước 2 phải đang chạy thì mới có kết quả.

---

## 4. Pipeline tổng thể

```
Câu nhập vào (bất kỳ ngôn ngữ)
        │
        ▼
  Tokenizer (XLM-R, SentencePiece) → tách câu thành subword token
        │
        ▼
  Transformer encoder (XLM-RoBERTa) → sinh vector biểu diễn cho mỗi token
        │
        ▼
  Classification head → dự đoán nhãn BIO cho mỗi token (O, B-PER, I-PER, ...)
        │
        ▼
  Aggregation (gộp subword liên tiếp cùng nhãn thành 1 thực thể hoàn chỉnh)
        │
        ▼
  JSON {text, label, start, end, score} → trả về frontend
        │
        ▼
  JS vẽ lại câu, mỗi thực thể được gạch chân màu + gắn tag (kiểu interlinear gloss)
```

---

## 5. Lý thuyết mô hình

### 5.1 NER là bài toán gì

Named Entity Recognition là một dạng  **sequence labeling** : mỗi token
trong câu được gán một nhãn, không phải gán nhãn cho cả câu như bài toán
phân loại văn bản thông thường. Schema nhãn dùng ở đây là  **BIO** :

* `O` — không thuộc thực thể nào
* `B-X` — token đầu tiên của một thực thể loại X
* `I-X` — token tiếp theo, vẫn thuộc thực thể loại X đó

### 5.2 Vì sao chọn XLM-RoBERTa

* **mBERT** (multilingual BERT) chỉ pretrain trên Wikipedia của từng
  ngôn ngữ — với ngôn ngữ ít tài nguyên như tiếng Việt, lượng dữ liệu
  pretrain khá mỏng.
* **XLM-RoBERTa** pretrain trên CC-100 (dữ liệu lọc từ CommonCrawl, quy
  mô lớn hơn Wikipedia rất nhiều ở hầu hết ngôn ngữ), dùng tokenizer
  SentencePiece với vocab 250k dùng chung cho mọi ngôn ngữ, và áp dụng
  cách train hiệu quả hơn từ RoBERTa (bỏ Next Sentence Prediction, train
  lâu hơn, batch lớn hơn). Kết quả là XLM-R vượt mBERT rõ rệt nhất ở các
  ngôn ngữ ít tài nguyên — đúng tình huống tiếng Việt so với tiếng Anh
  trong project này.

### 5.3 Vì sao cần "align" nhãn với subword token

Transformer không xử lý nguyên một từ — nó tách từ thành các subword
(ví dụ "Honolulu" → "Ho", "no", "lulu"). Nhưng dữ liệu WikiANN chỉ gán
nhãn ở cấp từ. Script xử lý bằng cách: subword đầu tiên của một từ giữ
nhãn thật, các subword tiếp theo của từ đó được gán `-100` để hàm loss bỏ
qua, không tính nhầm — đây là cách chuẩn theo tutorial chính thức của
Hugging Face cho token classification.

Đánh đổi của cách này: model không được giám sát trực tiếp ở các vị trí
subword giữa/cuối từ, nên đôi khi dự đoán ở những vị trí đó không nhất
quán (nhất là với từ hiếm/từ không có trong tập train). Cách giảm ảnh
hưởng lúc inference là dùng `aggregation_strategy="first"` trong pipeline
— chỉ tin vào nhãn của subword đầu tiên cho cả từ, bỏ qua nhiễu từ các
subword sau.

### 5.4 Vì sao đánh giá bằng seqeval, không dùng accuracy

Phần lớn token trong một câu là `O` (không phải thực thể), nên accuracy
thường rất cao một cách "giả" (model chỉ cần đoán đúng phần `O` là đã ăn
điểm). **seqeval** tính precision/recall/F1 theo đúng span thực thể hoàn
chỉnh, phản ánh đúng khả năng nhận diện thực thể của model hơn nhiều.

### 5.5 Checkpoint, early stopping, model chính thức

* `save_total_limit=1`: mỗi lần lưu checkpoint mới, Trainer tự xóa
  checkpoint cũ, chỉ giữ checkpoint gần nhất trên đĩa.
* `load_best_model_at_end=True` + `metric_for_best_model="f1"`: sau khi
  train xong, Trainer tự nạp lại đúng checkpoint có F1 validation cao
  nhất, không phải checkpoint cuối cùng theo thời gian.
* `EarlyStoppingCallback`: tự dừng train nếu F1 validation không cải
  thiện sau một số epoch liên tiếp, tránh train dư thời gian không cần
  thiết.
* Sau khi train, model tốt nhất được lưu riêng vào `./mner-production`
  (chỉ gồm weight + tokenizer, không có optimizer/scheduler state) —
  đây là bản "chính thức" mà `backend.py` load để serve, độc lập với các
  checkpoint tạm đã bị xóa.

---

## 6. Một số lỗi thường gặp

| Hiện tượng                                                                     | Nguyên nhân                                                                              | Cách sửa                                                                  |
| --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------- |
| `Failed to fetch`trên web                                                      | Backend chưa chạy hoặc chạy sai cách (`python backend.py`thay vì `uvicorn`)      | Chạy `uvicorn backend:app --port 8000`                                   |
| `Can't initialize NVML`                                                         | Cảnh báo từ thư viện giám sát GPU, không phải lỗi CUDA                           | Kiểm tra `torch.cuda.is_available()`— nếu `True`thì bỏ qua được |
| Thực thể bị tách rời, gán nhãn lẫn lộn (vd `Go(PER)ose(ORG)wor(PER)x`) | Subword giữa/cuối từ không được giám sát nhãn lúc train                         | Đổi `aggregation_strategy`sang `"first"`trong `backend.py`          |
| `MISSING: classifier.weight/bias`khi load model                                 | Bình thường — đầu phân loại NER mới được khởi tạo, sẽ học trong lúc train | Không cần sửa gì                                                        |
