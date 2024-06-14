import tkinter as tk
from tkinter import scrolledtext, messagebox
from assistant.gpt_assistant import generate_questions
from assistant.voice_interaction import recognize_speech, speak_text
from fpdf import FPDF
import threading

def log_conversation(user_input, assistant_response, log):
    log.append(f"You: {user_input}\n")
    log.append(f"Assistant: {assistant_response}\n")

def save_conversation_to_pdf(conversation_log, filename="interview_chat.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for line in conversation_log:
        pdf.multi_cell(0, 10, line)
    pdf.output(filename)
    messagebox.showinfo("Save PDF", "The interview chat has been saved to a PDF file.")

def update_log(text):
    log.insert(tk.END, text + "\n")
    log.yview(tk.END)

def start_interview():
    def run_interview():
        speak_text("Hello there! I'm your friendly interview bot. What's your name?")
        update_log("Hello there! I'm your friendly interview bot. What's your name?")
        name = recognize_speech()
        update_log(f"User: {name}")
        speak_text(f"Nice to meet you, {name}! Let's get started with your interview.")

        while True:
            speak_text("What topic would you like to discuss today?")
            update_log("What topic would you like to discuss today?")
            topic = recognize_speech()
            update_log(f"User selected topic: {topic}")

            if topic.lower() == 'exit':
                speak_text("Alright, have a great day! Goodbye!")
                update_log("Alright, have a great day! Goodbye!")
                break

            speak_text(f"Great choice, {name}! Let's talk about {topic}.")
            update_log(f"Great choice, {name}! Let's talk about {topic}.")

            questions = generate_questions(topic)

            if not questions:
                speak_text("Hmm, I couldn't find questions on that topic. Could you please try a different one?")
                update_log("Hmm, I couldn't find questions on that topic. Could you please try a different one?")
                continue

            conversation_log = []
            positive_responses = [
                "That's really interesting!",
                "Thank you for sharing that!",
                "I appreciate your insights!",
                "That's a great point!",
                "Well said!"
            ]

            for i, question in enumerate(questions):
                speak_text(f"Here's question number {i + 1}: {question}")
                update_log(f"Question {i + 1}: {question}")
                response = recognize_speech()
                update_log(f"User response: {response}")

                positive_response = positive_responses[i % len(positive_responses)]
                speak_text(positive_response)
                update_log(positive_response)

                log_conversation(question, response, conversation_log)

            speak_text("Thanks for your responses! You did a great job answering the questions.")
            update_log("Interview finished. Thank you for your responses.")

            save_conversation_to_pdf(conversation_log)
            speak_text("I've saved our conversation to a PDF file for you.")
            update_log("The interview chat has been saved to a PDF file.")
            break

    interview_thread = threading.Thread(target=run_interview)
    interview_thread.start()

def on_start():
    start_button.config(state=tk.DISABLED)
    start_interview()

def on_exit():
    root.quit()

# GUI setup
root = tk.Tk()
root.title("Friendly Voice Assistant Interview Bot")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(pady=10)

log_frame = tk.LabelFrame(frame, text="Conversation Log", padx=10, pady=10)
log_frame.pack(fill="both", expand="yes")

log = scrolledtext.ScrolledText(log_frame, width=80, height=20, state='normal')
log.pack()

control_frame = tk.Frame(frame)
control_frame.pack(pady=10)

start_button = tk.Button(control_frame, text="Start Interview", command=on_start)
start_button.pack(side=tk.LEFT, padx=5)

exit_button = tk.Button(control_frame, text="Exit", command=on_exit)
exit_button.pack(side=tk.RIGHT, padx=5)

root.mainloop()