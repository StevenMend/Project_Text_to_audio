import PyPDF2
from gtts import gTTS
import tkinter as tk
from tkinter import filedialog, messagebox
import os

def extract_text_from_pdf(pdf_file):
    try:
        with open(pdf_file, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error reading PDF file: {e}")
        return None

def convert_text_to_audio(text, output_audio_file, language):
    try:
        tts = gTTS(text=text, lang=language)
        tts.save(output_audio_file)
        return output_audio_file  # Return the generated file
    except Exception as e:
        messagebox.showerror("Error", f"Error converting text to audio: {e}")

def pdf_to_audiobook(pdf_file, language):
    print(f"Extracting text from {pdf_file}...")
    text = extract_text_from_pdf(pdf_file)

    if text:
        print("Converting text to audiobook...")
        output_audio_file = convert_text_to_audio(text, 'audiobook.mp3', language)
        if output_audio_file:
            download_button.config(state=tk.NORMAL)  # Enable download button
            return output_audio_file
    return None

# Function to select the PDF file
def select_pdf_file():
    pdf_file = filedialog.askopenfilename(title="Select PDF File", filetypes=[("PDF files", "*.pdf")])
    if pdf_file:
        pdf_file_entry.delete(0, tk.END)  # Clear the text field
        pdf_file_entry.insert(0, pdf_file)  # Insert the path of the selected PDF file

# Function to generate the audiobook
def generate_audiobook():
    pdf_file = pdf_file_entry.get()
    language = language_var.get()

    if pdf_file:
        output_audio_file = pdf_to_audiobook(pdf_file, language)
        if output_audio_file:
            messagebox.showinfo("Success", f"Audiobook generated: {output_audio_file}")
    else:
        messagebox.showwarning("Warning", "Please select a PDF file.")

def download_audiobook():
    output_audio_file = 'audiobook.mp3'

    save_path = filedialog.asksaveasfilename(defaultextension=".mp3", initialfile=output_audio_file,
                                             filetypes=[("MP3 files", "*.mp3"), ("All files", "*.*")])
    if save_path:
        try:
            os.rename(output_audio_file, save_path)
            messagebox.showinfo("Success", "Audiobook downloaded successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving the audiobook: {e}")

root = tk.Tk()
root.title("PDF to Audiobook")
root.geometry("400x350")  # Window size

# Create and place the widgets
tk.Label(root, text="Select PDF file:", font=("Arial", 12)).pack(pady=10)

pdf_file_entry = tk.Entry(root, width=50, font=("Arial", 10))
pdf_file_entry.pack(pady=5)

tk.Button(root, text="Browse PDF", command=select_pdf_file, font=("Arial", 10)).pack(pady=5)

# Language selection
tk.Label(root, text="Select Language:", font=("Arial", 12)).pack(pady=10)

language_var = tk.StringVar(value='en')  # Default language is English
tk.Radiobutton(root, text="English", variable=language_var, value='en').pack(anchor=tk.W)
tk.Radiobutton(root, text="Spanish", variable=language_var, value='es').pack(anchor=tk.W)
tk.Radiobutton(root, text="French", variable=language_var, value='fr').pack(anchor=tk.W)

tk.Button(root, text="Generate Audiobook", command=generate_audiobook, font=("Arial", 10)).pack(pady=10)

download_button = tk.Button(root, text="Download Audiobook", command=download_audiobook, font=("Arial", 10),
                            state=tk.DISABLED)
download_button.pack(pady=10)

root.mainloop()
