import customtkinter as ctk
import pandas as pd
import pywhatkit as kit
import time
import random
import threading
from tkinter import filedialog, messagebox


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("WhatsApp Bulk Sender 💬")
app.geometry("550x520")
app.resizable(False, False)


file_path = ""
pause_flag = False
current_index = 0


def browse_file():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    entry_file.delete(0, "end")
    entry_file.insert(0, file_path)


def toggle_pause():
    global pause_flag

    pause_flag = not pause_flag

    if pause_flag:
        stop_btn.configure(text="Continue ▶️", fg_color="green")
        status_label.configure(text="⏸ Paused (You can edit message)")
    else:
        stop_btn.configure(text="Stop ⛔", fg_color="red")
        status_label.configure(text="▶️ Resuming...")

def send_messages():
    global current_index, pause_flag

    message = textbox.get("1.0", "end").strip()

    if not file_path or not message:
        messagebox.showerror("Error", "Please select a file and enter a message.")
        return

    send_btn.configure(state="disabled")

    def task():
        global current_index, pause_flag

        try:
            data = pd.read_excel(file_path)
            total = len(data)

            BASE_DELAY = 20
            RANDOM_DELAY = 10
            BATCH_SIZE = 5
            LONG_BREAK = 60

            i = current_index

            while i < total:

              
                if pause_flag:
                    current_index = i
                    time.sleep(1)
                    continue

                phone = str(data.iloc[i, 0]).strip()

                if not phone.isdigit():
                    i += 1
                    continue

                status_label.configure(text=f"Sending {i+1}/{total} → {phone}")
                progress.set((i + 1) / total)
                app.update_idletasks()

                success = False

             
                for attempt in range(2):
                    try:
                        kit.sendwhatmsg_instantly(
                            f"+{phone}",
                            textbox.get("1.0", "end").strip(),
                            wait_time=10,
                            tab_close=True
                        )
                        success = True
                        break
                    except Exception as e:
                        print(f"Retry {attempt+1}: {e}")
                        time.sleep(8)

                if not success:
                    print(f"Failed → {phone}")

                delay = BASE_DELAY + random.randint(0, RANDOM_DELAY)
                time.sleep(delay)

             
                if (i + 1) % BATCH_SIZE == 0:
                    status_label.configure(text="😴 Taking break...")
                    time.sleep(LONG_BREAK)

                i += 1
                current_index = i

            messagebox.showinfo("Done", "Messages sent successfully ✅")

        except Exception as e:
            messagebox.showerror("Error", str(e))

        finally:
            send_btn.configure(state="normal")

    threading.Thread(target=task).start()

# ---------------- UI ----------------
title = ctk.CTkLabel(app, text="WhatsApp Bulk Sender", font=("Arial", 22, "bold"))
title.pack(pady=15)

entry_file = ctk.CTkEntry(app, width=420, placeholder_text="Choose Excel file")
entry_file.pack(pady=10)

browse_btn = ctk.CTkButton(app, text="Browse 📂", command=browse_file)
browse_btn.pack(pady=5)

textbox = ctk.CTkTextbox(app, width=450, height=120)
textbox.pack(pady=10)

send_btn = ctk.CTkButton(app, text="Send 🚀", command=send_messages)
send_btn.pack(pady=10)

stop_btn = ctk.CTkButton(app, text="Stop ⛔", command=toggle_pause, fg_color="red")
stop_btn.pack(pady=5)

progress = ctk.CTkProgressBar(app, width=450)
progress.pack(pady=10)
progress.set(0)

status_label = ctk.CTkLabel(app, text="")
status_label.pack(pady=5)

app.mainloop()