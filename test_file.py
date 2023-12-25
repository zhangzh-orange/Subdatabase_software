import tkinter as tk

def show_window1():
    window1 = tk.Toplevel(root)
    window1.title("Window 1")

    def on_choice1():
        result_label.config(text="You chose 1")

    def on_choice2():
        result_label.config(text="2")

    def on_choice3():
        result_label.config(text="Please do not choose it")

    button1 = tk.Button(window1, text="Choose 1", command=on_choice1)
    button1.pack()

    button2 = tk.Button(window1, text="Choose 2", command=on_choice2)
    button2.pack()

    button3 = tk.Button(window1, text="Choose 3", command=on_choice3)
    button3.pack()

    result_label = tk.Label(window1, text="")
    result_label.pack()

def show_window2():
    window2 = tk.Toplevel(root)
    window2.title("Window 2")
    label = tk.Label(window2, text="This is Window 2")
    label.pack()

def on_submit():
    try:
        user_input = int(entry.get())
        if user_input == 1:
            show_window1()
        else:
            show_window2()
    except ValueError:
        # Handle the case where the user input is not a valid integer
        error_label.config(text="Please enter a valid number")

# Main window
root = tk.Tk()
root.title("Main Window")

# Widgets
label = tk.Label(root, text="Enter a number:")
label.pack()

entry = tk.Entry(root)
entry.pack()

submit_button = tk.Button(root, text="Submit", command=on_submit)
submit_button.pack()

error_label = tk.Label(root, text="", fg="red")
error_label.pack()

# Start the GUI main loop
root.mainloop()