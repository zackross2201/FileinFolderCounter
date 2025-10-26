import os
import collections
import time
import tkinter as tk
from tkinter import filedialog

def count_files_in_directory(directory_path, output_text_widget):
    """
    Recursively counts all files in a given directory and provides
    a breakdown by file extension. Outputs results to the text_widget.
    """
    
    def log(message):
        """Helper function to print to GUI and console (for debugging)."""
        print(message)
        output_text_widget.insert(tk.END, message + "\n")
        output_text_widget.see(tk.END) # Auto-scroll to bottom
        output_text_widget.update_idletasks() # Force GUI update

    # Clear previous results
    output_text_widget.delete('1.0', tk.END)

    total_file_count = 0
    total_folder_count = 0
    extension_counts = collections.defaultdict(int)

    log(f"Scanning files in '{directory_path}'...")
    log("This may take a moment for large directories...")
    
    start_time = time.time()

    try:
        # os.walk() recursively visits every directory and subdirectory
        for dirpath, dirnames, filenames in os.walk(directory_path, topdown=True, onerror=None):
            total_folder_count += len(dirnames)
            for filename in filenames:
                total_file_count += 1
                extension = os.path.splitext(filename)[1].lower()
                extension_counts[extension] += 1
        
        end_time = time.time()
        duration = end_time - start_time

        # --- Printing the final report ---
        log("\n--- Scan Complete ---")
        log(f"Scanned {total_folder_count:,} folders and {total_file_count:,} files in {duration:.2f} seconds.")

        if total_file_count > 0:
            log("\n--- File Type Breakdown (most common first) ---")
            
            sorted_extensions = sorted(extension_counts.items(), key=lambda item: item[1], reverse=True)
            
            for extension, count in sorted_extensions:
                if extension == "":
                    log(f"  {count:>10,} files with no extension")
                else:
                    log(f"  {count:>10,} {extension} files")
        
        log("\n" + "=" * 50)
        log("Ready for a new scan. Please select a folder.")

    except PermissionError:
        log(f"\n--- ERROR ---")
        log(f"Permission denied. You don't have permission to access part of '{directory_path}'.")
    except Exception as e:
        log(f"\n--- An unexpected error occurred ---")
        log(f"{e}")

def ask_for_directory(text_widget):
    """
    Opens a folder-picker dialog and then triggers the count.
    """
    # Ask the user to select a directory
    directory_path = filedialog.askdirectory()
    
    # If the user didn't cancel the dialog
    if directory_path:
        count_files_in_directory(directory_path, text_widget)
    else:
        text_widget.insert(tk.END, "Scan cancelled by user.\n")
        print("Scan cancelled by user.")

def main():
    """
    Main function to create and run the GUI app.
    """
    # Set up the main window
    root = tk.Tk()
    root.title("Folder File Counter")
    root.geometry("700x500") # Set a default size

    # Create a frame for the button
    top_frame = tk.Frame(root, pady=10)
    top_frame.pack(side=tk.TOP, fill=tk.X)

    # Create the "Select Folder" button
    browse_button = tk.Button(
        top_frame,
        text="Click Here to Select a Folder to Scan",
        font=("Arial", 12, "bold"),
        padx=10,
        pady=5,
        command=lambda: ask_for_directory(output_text) # Pass the text widget
    )
    browse_button.pack()

    # Create a frame for the text output area
    # *** THIS IS THE FIXED LINE ***
    # Changed pady=(0, 10) to pady=10 to avoid the TclError
    text_frame = tk.Frame(root, padx=10, pady=10)
    text_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    # Create a scrollbar
    scrollbar = tk.Scrollbar(text_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Create the text widget for output
    output_text = tk.Text(
        text_frame,
        wrap=tk.WORD, # Wrap text at word boundaries
        font=("Courier New", 10),
        yscrollcommand=scrollbar.set # Link scrollbar
    )
    output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Configure the scrollbar
    scrollbar.config(command=output_text.yview)

    # Add initial instructions
    output_text.insert(tk.END, "Welcome to the File Counter App!\n\n")
    output_text.insert(tk.END, "Please click the button above to select a folder.\n")
    output_text.insert(tk.END, "The results of the scan will appear here.\n")

    # Start the GUI event loop
    root.mainloop()

# Run the main function when the script is executed
if __name__ == "__main__":
    main()

