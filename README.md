# ⚡ Smart Meter Tamper & Fault Detection System

This project detects **faulty or tampered smart meters** and identifies the **root cause** using **Microsoft Phi-3 Mini (4k)** model with **LoRA fine-tuning**. It includes a **Django-based UI** for monitoring, data viewing, and email alerts, and features a **RAG-powered chatbot** that explains meter metrics in plain English.

---

## 🚀 Features

- ⚙️ **Tamper & fault detection** via fine-tuned Phi-3 Mini model
- 🧠 **RAG chatbot** to explain meter metrics & anomalies
- 🌐 **Django web dashboard** for real-time monitoring
- 📬 **Email alert system** for suspected tampering
- 📊 **Interactive data viewer** for smart meter logs

---

## 🛠️ Tech Stack

- **Backend**: Django, Django REST Framework
- **LLM**: Microsoft Phi-3 Mini 4k (with LoRA adapter)
- **RAG**: Local context retrieval + lightweight embedding store
- **Frontend**: Django templates
- **Notifications**: SMTP email for tamper alerts
- **Database**: SQLite

---

## ⚙️ Setup

### 1. Clone the repo

```bash
git clone https://github.com/Bharath-vs-07/Fault-meter-detection-using-Microsoft-phi-3-mini-with-LoRA.git
