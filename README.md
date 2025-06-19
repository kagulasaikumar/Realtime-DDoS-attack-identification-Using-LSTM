# Real-Time DDoS Attack Identification using LSTM

This project focuses on detecting **Distributed Denial of Service (DDoS)** attacks in **real-time** using a deep learning-based **LSTM (Long Short-Term Memory)** model.
It monitors simulated network traffic, identifies suspicious patterns, generates alerts, and simulates mitigation — all in a real-time setup.

---

## Project Overview

- Real-time DDoS detection using time-series traffic data and an LSTM model.
- Simulates detection alerts and mitigation logic during live input evaluation.
- Achieves over **95% accuracy** in classifying normal vs. DDoS traffic.
- Built and executed entirely on **Google Colab** for accessibility and performance.
- Integrates a basic UI for live monitoring of results.
---

## Technologies Used

- **Language:** Python  
- **Deep Learning:** TensorFlow, Keras  
- **Data Handling:** Pandas, NumPy  
- **Visualization:** Matplotlib, Seaborn  
- **Development Platform:** Google Colab  
- **Execution Mode:** Real-time simulation with console-based alerts

---
##  User Interface (UI)

A minimal UI was developed to visualize:
- Live attack detection alerts
- Normal vs. malicious packet flow indicators
- Real-time logs and system status updates

The UI allows users to:
- Upload sample datasets or simulate traffic
- Monitor predictions and threat levels
- Understand the model’s decision-making clearly

*Note: The UI was built using basic Python tools (like Streamlit / Tkinter / Flask) depending on environment support.*
