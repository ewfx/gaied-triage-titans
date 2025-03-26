# 🚀 Project Name

## 📌 Table of Contents
- [Introduction](#introduction)
- [Demo](#demo)
- [Inspiration](#inspiration)
- [What It Does](#what-it-does)
- [How We Built It](#how-we-built-it)
- [Challenges We Faced](#challenges-we-faced)
- [How to Run](#how-to-run)
- [Tech Stack](#tech-stack)
- [Team](#team)

---

## 🎯 Introduction
A brief overview of your project and its purpose. Mention which problem statement are your attempting to solve. Keep it concise and engaging.

## 🎥 Demo
🔗 [Live Demo](#) (if applicable)  
📹 [Video Demo]('Screen Recording 2025-03-26 at 5.44.07 PM.mov') (if applicable)  
🖼️ Screenshots:

![App](/images/image.png)

## 💡 Inspiration
We're solving email classification and routing to respective teams responsible for handling the requests.

## ⚙️ What It Does
This project fetches emails from a directory, where it is downloaded, reads through it and classifies it into its primary request type.

## 🛠️ How We Built It
We have used a pre-trained LLM - FLAN-T5, an enhanced version of T5 to handle the prompts to classify the emails.

## 🚧 Challenges We Faced
Data gathering.

## 🏃 How to Run
1. Clone the repository  
   ```sh
   git clone https://github.com/your-repo.git
   ```
2. To setup the backend
   1. Create a python virtual environment(macOS)
      ```sh
      python3 -m venv venv
      ```
   2. Activate the virtual environment(macOS)
      ```sh
      source ./venv/bin/activate
      ```
   3. cd into backend directory
      ```sh
      cd code/src/backend
      ```
   4. create a `emails` folder and download the emails into it
   5. install the required packages
      ```sh
      pip install -r requirements.txt
      ```
   6. run the flask app server
      ```sh
      python3 app.py
      ```
3. To setup the frontend
   1. cd into frontend directory
      ```sh
      cd code/src/frontend
      ```
   2. install the required packages
      ```sh
      npm install
      ```
   3. start the app
      ```
      npm start
      ```

## 🏗️ Tech Stack
- 🔹 Frontend: React
- 🔹 Backend: Flask

## 👥 TriageTitans
- **Prabhakar Das**
- **Gyanendra Kumar**
- **Ankur Jain**
- **Abhishek Paul**
- **Sunil Ashwathanarayana**