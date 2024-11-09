from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import random

# Initialize Tkinter window
root = Tk()
root.title('Undead or Alive Card Shuffler')
root.geometry("600x500")  # Increase window size for both piles

# List of image paths (library pile)
image_paths = [
    "images/thrasta-tempest-s-roar.jpg", 
    "images/thundering-spineback.jpg",
    "images/wakening-sun-s-avatar.jpg"
]

# Discard pile (initially empty)
discard_pile = []
discard_count = len(discard_pile)

# Library pile (initially same as image_paths)
library_pile = image_paths.copy()
library_count = len(library_pile)

# Starting image index (current image in the library)
current_image_index = 0

# Starting image size
display_width = 150
display_height = 210

# Function to display the image at a given size
def display_image(image_path, row, column):
    try:
        # Open the image using PIL
        img = Image.open(image_path)
        img = img.resize((display_width, display_height))  # Resize image
        img_tk = ImageTk.PhotoImage(img)  # Convert to a Tkinter-compatible photo image

        # Create or update the label widget to hold the image
        label = Label(root, image=img_tk)
        label.image = img_tk  # Keep reference to the image to prevent garbage collection
        label.grid(row=row, column=column)  # Position the image at (row, column)

    except Exception as e:
        print(f"Error loading image: {e}")

# Shuffle the cards in the library, display first card
def shuffle_library():
    global current_image_index
    random.shuffle(library_pile)
    current_image_index = 0  # Reset to the first image after shuffling
    update_display()

# Function to update the display for the discard pile
def update_discard_pile():
    # Clear the previous discard display
    for widget in root.grid_slaves():
        if int(widget.grid_info()["row"]) == 1 and int(widget.grid_info()["column"]) == 2:
            widget.destroy()  # Clear previous discard pile image

    if discard_pile:
        for idx, image_path in enumerate(discard_pile):
            display_image(image_path, row=1, column=2)
    else:
        display_image("images/card-back.jpg", row=1, column=2)  # Show card back if empty

# Move the top card from library to discard
def move_to_discard():
    global current_image_index
    if library_pile:
        top_of_deck = library_pile[0]
        
        # Check if the image path is already in the discard pile to prevent duplicates
        if top_of_deck not in discard_pile:
            discard_pile.insert(0, top_of_deck)
            library_pile.pop(0)  # Remove from library pile
            current_image_index = 0  # Reset to first image after discard
            update_display()
        else:
            messagebox.showinfo("Error", "This card is already in the discard pile.")
    else:
        messagebox.showinfo("Error", "Library pile is empty.")

# Update the count labels and display the current images
def update_display():
    global discard_count, library_count

    # Clear the previous library and discard displays
    for widget in root.grid_slaves():
        if int(widget.grid_info()["row"]) == 1:
            widget.destroy()  # Clear all images

    # Update image for the library pile
    if library_pile:
        display_image(library_pile[current_image_index], row=1, column=1)

    # Update the discard pile display
    update_discard_pile()

# Reset cards in library and discard
def reset():
    global current_image_index, discard_pile, library_pile

    current_image_index = 0
    discard_pile = []
    library_pile = image_paths.copy()
    update_display()

# Display the initial image (first card in the library pile)
update_display()

# Buttons to navigate images
button_shuffle = Button(root, text="Shuffle", command=shuffle_library)
button_exit = Button(root, text="Exit", command=root.quit)
button_discard = Button(root, text=">>", command=move_to_discard)
button_reset = Button(root, text="Reset", command=reset)

# Position the buttons on the window
button_shuffle.grid(row=2, column=0)
button_exit.grid(row=2, column=1)
button_discard.grid(row=2, column=2)
button_reset.grid(row=3, column=0)

# Label to show counts
current_image_index_label = Label(text=f"Image Index: {current_image_index}")
library_count_label = Label(text=f"Library: {library_count}")
discard_count_label = Label(text=f"Discard: {discard_count}")

# Position the count labels
current_image_index_label.grid(row=0, column=0)
library_count_label.grid(row=0, column=1)
discard_count_label.grid(row=0, column=2)

# Start the Tkinter event loop
root.mainloop()
