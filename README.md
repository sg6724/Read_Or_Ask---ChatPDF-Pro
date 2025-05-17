# 📚 ChatPDF Pro

### *Read. Chat. Understand.*

Ever wished you could *talk* to your PDFs?
**ChatPDF Pro** makes it happen. Upload a PDF, ask questions, and get instant answers from your documents—like magic, but open-source.

---

## 🚀 Why ChatPDF Pro?

Let’s be real—digging through long PDFs is painful. Whether it's a 200-page research paper, legal contract, or tech manual, **ChatPDF Pro** turns that nightmare into a breeze:

✅ Chat with your PDF like you're texting a friend
✅ Fast, accurate answers with Gemini + FAISS vector search
✅ Clean, modern UI with Streamlit
✅ Fully local & open source — your data stays yours
✅ Easy to extend, built for hackers and pros alike

---

## 🧠 How It Works



1. **Upload** any PDF
2. **Parse** with blazing-fast PyMuPDF
3. **Chunk** content into smart segments
4. **Embed** with Gemini and store in **FAISS**
5. **Ask** questions and get contextual answers via **LangChain + Gemini**
6. **Streamlit** powers the frontend

---

## 🛠️ Stack

| Layer             | Tech                      |
| ----------------  | ------------------------- |
| 🔍 Parsing       | PyPDF2                   |
| 🧠 Embedding     | Ollama                   |
| 🗃️ Storage       | FAISS + SQLModel (SQLite) |
| 🤖 Backend       | python                   |
| 🖼️ Frontend      | Streamlit                 |
| 🧩 Orchestration | LangChain                |

---



## 📌 Roadmap

* [x] Basic PDF upload & parsing
* [x] Chat interface with context
* [x] Local FAISS vector store
* [ ] Summarization mode
* [ ] Support for multi-PDF querying
* [ ] User auth & upload history

