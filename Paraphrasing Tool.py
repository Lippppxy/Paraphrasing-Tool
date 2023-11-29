import tkinter as tk
from tkinter import messagebox
from openai import OpenAI

# Setelah mendapatkan API key dari OpenAI, atur sebagai berikut
openai_api_key = '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'
client = OpenAI(api_key=openai_api_key)

def process_text_input(prompt, min_tokens=5):
    # Tambahkan panduan untuk parafrase
    paraphrase_prompt = "Parafasekan teks berikut dengan mengganti kata-kata dan merubah urutan kalimatnya agar tetap relevan:\n"
    
    # Gabungkan prompt, panduan parafrase, dan konteks sebelumnya
    full_prompt = ' '.join([paraphrase_prompt, prompt])

    completion = client.completions.create(
        model='text-davinci-003',
        prompt=full_prompt,
        temperature=0.2,
        max_tokens=3000
    )
    response_tokens = completion.choices[0].text.split()
    response = ' '.join(response_tokens[:max(min_tokens, len(response_tokens))])
    
    return response

def on_submit(entry, output_text):
    user_input = entry.get("1.0", tk.END)  # Ambil teks dari widget Text
    user_input = user_input.strip()  # Hilangkan spasi di awal dan akhir teks
    if user_input.lower() == "exit":
        root.destroy()
    else:
        output_text.delete(1.0, tk.END)
        
        response = process_text_input(user_input)
        output_text.insert(tk.END, f"Hasil Parafrase: {response}\n")
        entry.delete(1.0, tk.END)  # Menghapus teks dari widget Text

def copy_to_clipboard(output_text):
    result_text = output_text.get("1.0", tk.END)
    result_text = result_text.replace("Hasil Parafrase: ", "")
    root.clipboard_clear()
    root.clipboard_append(result_text)
    root.update()

root = tk.Tk()
root.title("Parafrase Tool by Alip")

input_entry = tk.Text(root, wrap="word", height=5, width=50)
input_entry.pack(pady=10)

output_text = tk.Text(root, wrap="word", height=10, width=50)
output_text.pack(pady=10)

submit_button = tk.Button(root, text="Submit", command=lambda: on_submit(input_entry, output_text))
submit_button.pack()

copy_button = tk.Button(root, text="Copy", command=lambda: copy_to_clipboard(output_text))
copy_button.pack()

root.mainloop()