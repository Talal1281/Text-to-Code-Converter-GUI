import customtkinter as ctk
import pyperclip
import webbrowser
import os

def main_app():
    def link(url):
        webbrowser.open_new_tab("https://www.linkedin.com/in/talal-malhi/")

    def error_popup(message):
        popup = ctk.CTkToplevel()
        popup.title("Message")
        popup.geometry("400x300")
        label = ctk.CTkLabel(popup, text=message, wraplength=380)
        label.pack(pady=20, padx=20)
        ok_button = ctk.CTkButton(popup, text="OK", command=popup.destroy)
        ok_button.pack(pady=10)
        popup.mainloop()

    history = {
        "Morse": [],
        "ASCII": [],
        "Binary": []
    }

    def update_history(input_text, output_text, conversion_type):
        if conversion_type in history:
            history[conversion_type].append((input_text, output_text))
            if len(history[conversion_type]) > 50: 
                history[conversion_type].pop(0)

    def save_history_to_file():
        def save_file():
            filename = file_name_input.get("1.0", "end-1c").strip()
            if not filename:
                error_popup("File name cannot be empty.")
                return

            if not filename.endswith(".txt"):
                filename += ".txt"

            try:
                with open(filename, "w") as file:
                    for conversion_type, records in history.items():
                        file.write(f"{conversion_type} History:\n")
                        for record in records:
                            file.write(f"{record[0]} -> {record[1]}\n")
                        file.write("\n")
                error_popup(f"History saved to {filename}")
                save_popup.destroy()
            except Exception as e:
                error_popup(f"Error saving file: {e}")

        save_popup = ctk.CTkToplevel()
        save_popup.title("Save History")
        save_popup.geometry("400x200")
        ctk.CTkLabel(save_popup, text="Enter the file name for saving history:").pack(pady=10)
        file_name_input = ctk.CTkTextbox(save_popup, height=30, width=300)
        file_name_input.pack(pady=10)
        save_button = ctk.CTkButton(save_popup, text="Save", command=save_file)
        save_button.pack(pady=10)

    def view_combined_history():
        combined_history = ""
        for conversion_type, records in history.items():
            combined_history += f"{conversion_type} History:\n"
            combined_history += "\n".join(f"{inp} -> {outp}" for inp, outp in records) + "\n\n"

        history_popup = ctk.CTkToplevel()
        history_popup.title("View History")
        history_popup.geometry("600x400")

        text_area = ctk.CTkTextbox(history_popup, wrap="word", height=350, width=550)
        text_area.insert("1.0", combined_history or "No history available.")
        text_area.configure(state="disabled")
        text_area.pack(pady=20, padx=20)

        close_button = ctk.CTkButton(history_popup, text="Close", command=history_popup.destroy)
        close_button.pack(pady=10)

    def on_exit():
        if any(history.values()):
            save_prompt = ctk.CTkToplevel()
            save_prompt.title("Save History")
            save_prompt.geometry("400x200")

            label = ctk.CTkLabel(save_prompt, text="Your history will be deleted unless you save it. Do you want to save it?")
            label.pack(pady=20, padx=20)

            def save_and_exit():
                save_history_to_file()
                save_prompt.destroy()
                main_win.destroy()

            def exit_without_saving():
                save_prompt.destroy()
                main_win.destroy()

            save_button = ctk.CTkButton(save_prompt, text="Save and Exit", command=save_and_exit)
            save_button.pack(side="left", padx=20, pady=20)

            discard_button = ctk.CTkButton(save_prompt, text="Exit Without Saving", command=exit_without_saving)
            discard_button.pack(side="right", padx=20, pady=20)

            save_prompt.mainloop()
        else:
            main_win.destroy()

    def morse_code_window():
        morse_dict = {
            'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
            'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
            'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
            'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
            'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
            'Z': '--..', '1': '.----', '2': '..---', '3': '...--',
            '4': '....-', '5': '.....', '6': '-....', '7': '--...',
            '8': '---..', '9': '----.', '0': '-----', ' ': '/'
        }
        reverse_morse_dict = {v: k for k, v in morse_dict.items()}

        def clear_text():
            input_box.delete("1.0", "end")
            output_box.configure(state="normal")
            output_box.delete("1.0", "end")
            output_box.configure(state="disabled")

        def text_to_morse():
            text = input_box.get("1.0", "end-1c").upper()
            if not all(char in morse_dict for char in text.replace(' ', '')):
                error_popup("Only Morse code compatible characters allowed.")
                return
            morse_code = ' '.join(morse_dict[char] for char in text if char in morse_dict)
            output_box.configure(state="normal")
            output_box.delete("1.0", "end")
            output_box.insert("end", morse_code)
            output_box.configure(state="disabled")
            update_history(text, morse_code, "Morse")

        def morse_to_text():
            morse = input_box.get("1.0", "end-1c").strip()
            if not all(symbol in ['.', '-', ' ', '/'] for symbol in morse):
                error_popup("Please enter valid Morse code symbols only.")
                return
            text = ''.join(reverse_morse_dict.get(char, '') for char in morse.split())
            output_box.configure(state="normal")
            output_box.delete("1.0", "end")
            output_box.insert("end", text)
            output_box.configure(state="disabled")
            update_history(morse, text, "Morse")

        window = ctk.CTk()
        window.title("Morse Code Converter")
        window.geometry("600x400")

        ctk.CTkLabel(window, text="Enter Text or Morse Code:").pack()
        input_box = ctk.CTkTextbox(window, height=100, width=400)
        input_box.pack()

        to_morse_button = ctk.CTkButton(window, text="Convert to Morse", command=text_to_morse)
        to_morse_button.pack(fill='x')

        to_text_button = ctk.CTkButton(window, text="Convert to English", command=morse_to_text)
        to_text_button.pack(fill='x')

        clr_button = ctk.CTkButton(window, text="Clear", command=clear_text)
        clr_button.pack(fill='x')

        ctk.CTkLabel(window, text="Output:").pack()
        output_box = ctk.CTkTextbox(window, height=100, width=400, state="disabled")
        output_box.pack()

        window.mainloop()

    def ascii_window():
        def clear_text():
            input.delete("1.0", "end")
            output.configure(state="normal")
            output.delete("1.0", "end")
            output.configure(state="disabled")

        def text_to_ascii():
            text = input.get("1.0", "end-1c")
            ascii_codes = ' '.join(str(ord(char)) for char in text)
            output.configure(state="normal")
            output.delete("1.0", "end")
            output.insert("end", ascii_codes)
            output.configure(state="disabled")
            update_history(text, ascii_codes, "ASCII")

        def ascii_to_text():
            ascii_codes = input.get("1.0", "end-1c").strip().split()
            try:
                text = ''.join(chr(int(code)) for code in ascii_codes)
                output.configure(state="normal")
                output.delete("1.0", "end")
                output.insert("end", text)
                output.configure(state="disabled")
                update_history(' '.join(ascii_codes), text, "ASCII")
            except ValueError:
                error_popup("Invalid ASCII codes.")

        window = ctk.CTk()
        window.title('ASCII Converter')
        window.geometry("600x400")

        ctk.CTkLabel(window, text="Enter Text or ASCII:").pack()
        input = ctk.CTkTextbox(window, height=100, width=400)
        input.pack()

        text_button = ctk.CTkButton(window, text="Text to ASCII", command=text_to_ascii)
        text_button.pack(fill='x')

        num_button = ctk.CTkButton(window, text="ASCII to Text", command=ascii_to_text)
        num_button.pack(fill='x')

        clr_button = ctk.CTkButton(window, text="Clear", command=clear_text)
        clr_button.pack(fill='x')

        ctk.CTkLabel(window, text="Output:").pack()
        output = ctk.CTkTextbox(window, height=100, width=400, state="disabled")
        output.pack()

        window.mainloop()

    def binary_window():
        def clear_text():
            input.delete("1.0", "end")
            output.configure(state="normal")
            output.delete("1.0", "end")
            output.configure(state="disabled")

        def text_to_binary():
            text = input.get("1.0", "end-1c")
            binary = ' '.join(format(ord(char), '08b') for char in text)
            output.configure(state="normal")
            output.delete("1.0", "end")
            output.insert("end", binary)
            output.configure(state="disabled")
            update_history(text, binary, "Binary")

        def binary_to_text():
            binary = input.get("1.0", "end-1c").strip().split()
            try:
                text = ''.join(chr(int(bits, 2)) for bits in binary)
                output.configure(state="normal")
                output.delete("1.0", "end")
                output.insert("end", text)
                output.configure(state="disabled")
                update_history(' '.join(binary), text, "Binary")
            except ValueError:
                error_popup("Invalid binary codes.")

        window = ctk.CTk()
        window.title("Binary Converter")
        window.geometry("600x400")

        ctk.CTkLabel(window, text="Enter Text or Binary Code:").pack()
        input = ctk.CTkTextbox(window, height=100, width=400)
        input.pack()

        text_button = ctk.CTkButton(window, text="Text to Binary", command=text_to_binary)
        text_button.pack(fill='x')

        bin_button = ctk.CTkButton(window, text="Binary to Text", command=binary_to_text)
        bin_button.pack(fill='x')

        clr_button = ctk.CTkButton(window, text="Clear", command=clear_text)
        clr_button.pack(fill='x')

        ctk.CTkLabel(window, text="Output:").pack()
        output = ctk.CTkTextbox(window, height=100, width=400, state="disabled")
        output.pack()

        window.mainloop()

    main_win = ctk.CTk()
    main_win.title("Code Converters")
    main_win.geometry('500x400')
    main_win.resizable(1, 1)

    def front(text, command):
        btn = ctk.CTkButton(main_win, text=text, command=command, corner_radius=10)
        btn.pack(pady=10, padx=100, fill='x')
        return btn

    title_page = ctk.CTkLabel(main_win, text="Code Converters!", font=("Roboto", 24, "bold"))
    title_page.pack(pady=20)

    morse_button = front("Open Morse Code", command=morse_code_window)
    ascii_button = front("Open ASCII", command=ascii_window)
    binary_button = front("Open Binary", command=binary_window)

    view_history_button = front("View Combined History", command=view_combined_history)

    footer_frame = ctk.CTkFrame(main_win, fg_color="transparent") 
    footer_frame.pack(pady=30)

    copyright_label = ctk.CTkLabel(footer_frame, text="\u00a9 2024 Talal Malhi", font=("Roboto", 12))
    copyright_label.pack(side="left", padx=5)

    link_label = ctk.CTkLabel(footer_frame, text="Hover Over Me!", font=("Roboto", 12), cursor="hand2")
    link_label.pack(side="left", padx=5)
    link_label.bind("<Button-1>", lambda e: link("https://www.linkedin.com/in/talal-malhi/"))
    link_label.bind("<Enter>", lambda e: link_label.configure(text="Click Me To Learn More!"))
    link_label.bind("<Leave>", lambda e: link_label.configure(text="Hover Over Me!"))

    main_win.protocol("WM_DELETE_WINDOW", on_exit)
    main_win.mainloop()

main_app()
