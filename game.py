import tkinter as tk
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import os

# Global variables for player data and scores
players = []
scores = {}
bags = {}
current_round = 1
pdf_filename = "spades_scores.pdf"


# Function to create or update the PDF with scores in a tabular format
def create_or_update_pdf():
    # Check if the PDF already exists to know if we need to append new data
    is_new_file = not os.path.exists(pdf_filename)

    # Create a PDF document
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    elements = []

    # Create a header
    header = [["Round", "Player", "Round Score", "Total Score", "Bags"]]

    # Collect score data
    score_data = []
    for player_entry in players:
        player_name_str = player_entry.get().strip()  # Get player name for display
        round_score = scores[player_name_str]["round_score"]
        total_score = scores[player_name_str]["total_score"]
        bags_count = bags[player_name_str]
        score_data.append(
            [current_round, player_name_str, round_score, total_score, bags_count]
        )

    # Combine header and score data
    table_data = header + score_data

    # Create a table
    table = Table(table_data)
    style = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ]
    )

    table.setStyle(style)

    # If the file is new, add the header
    if is_new_file:
        elements.append(Table([["Spades Score Tracker"]], colWidths=[400]))
        elements.append(Table([[""]]))  # Add some space before the scores

    # Add the score table to elements
    elements.append(table)

    # Build the PDF
    doc.build(elements)


# Function to calculate score for each player
def calculate_score():
    global current_round
    try:
        total_bids_won = 0  # Initialize total bids won for the current round

        # First loop to validate tricks and calculate total bids won
        for player_entry in players:
            player_name_str = (
                player_entry.get().strip()
            )  # Get the player's name from the entry
            if player_name_str not in scores:
                messagebox.showerror(
                    "Error", f"Player {player_name_str} not found in scores."
                )
                return

            tricks = int(
                scores[player_name_str]["tricks_input"].get()
            )  # Get tricks from entry

            # Check if tricks exceed the current round number
            if tricks > current_round:
                messagebox.showerror(
                    "Error",
                    f"{player_name_str} has tricks exceeding the current round number. Please correct it.",
                )
                return

            total_bids_won += tricks  # Accumulate total bids won

        # Check if total bids won exceed the current round number
        if total_bids_won > current_round:
            messagebox.showerror(
                "Error",
                f"Total bids won ({total_bids_won}) exceed the current round number ({current_round}). Please enter tricks correctly.",
            )
            return

        # Second loop to calculate scores
        for player_entry in players:
            player_name_str = (
                player_entry.get().strip()
            )  # Get the player's name from the entry
            bid = int(scores[player_name_str]["bid_input"].get())  # Get bid from entry

            tricks = int(
                scores[player_name_str]["tricks_input"].get()
            )  # Get tricks from entry

            # Calculate round score and bags
            if tricks >= bid:
                # Player met or exceeded their bid
                round_score = (bid * 10) + (tricks - bid)  # Bids won - bids placed
                bags[player_name_str] += (
                    tricks - bid
                )  # Increment bags based on excess wins
            else:
                # Player lost their bid partially or totally
                round_score = -(bid * 10) + tricks

            # Update scores
            scores[player_name_str]["round_score"] = round_score
            scores[player_name_str]["total_score"] += round_score

        # Check for elimination
        for player_name_str in players:
            player_name_str = player_name_str.get().strip()  # Ensure it's a string
            if bags[player_name_str] >= 5:
                scores[player_name_str][
                    "display_name"
                ] = f"{player_name_str} (Eliminated)"
            else:
                scores[player_name_str]["display_name"] = player_name_str

        display_scores()
        create_or_update_pdf()  # Generate or update the PDF after calculating scores

        # Disable the calculate button after scores are calculated
        btn_calculate.config(state=tk.DISABLED)
        # Enable the next round button
        btn_next_round.config(state=tk.NORMAL)

    except ValueError:
        messagebox.showerror(
            "Input Error", "Please enter valid numbers for bids and tricks."
        )


# Function to display the updated scores on the interface
def display_scores():
    result_text = ""
    for player_entry in players:
        player_name_str = player_entry.get().strip()  # Get player name for display
        result_text += f"{scores[player_name_str]['display_name']}: Round Score = {scores[player_name_str]['round_score']}, Total Score = {scores[player_name_str]['total_score']}, Bags = {bags[player_name_str]}\n"
    lbl_result.config(text=result_text)


# Function to proceed to the next round
def next_round():
    global current_round
    current_round += 1

    if current_round > 13:
        # Create final score PDF and display total scores
        create_final_pdf()
        messagebox.showinfo(
            "Game Over",
            "The game has ended after 13 rounds. Total scores saved in PDF.",
        )
        root.quit()  # Exit the application after 13 rounds
    else:
        # Reset bids and tricks for the next round
        for player_name_str in players:
            player_name_str = player_name_str.get().strip()  # Ensure it's a string
            scores[player_name_str]["bid_input"].delete(0, tk.END)
            scores[player_name_str]["tricks_input"].delete(0, tk.END)
            scores[player_name_str]["round_score"] = 0

        setup_bids_tricks()  # Call to set up next round input fields
        btn_calculate.config(
            state=tk.NORMAL
        )  # Enable the calculate button for the new round
        btn_next_round.config(state=tk.DISABLED)  # Disable the next round button


# Function to create dynamic player entry fields for names
def setup_players():
    global players, scores, bags
    players = []
    scores = {}
    bags = {}

    try:
        num_players = int(entry_num_players.get())
        if num_players < 2:
            raise ValueError("Must have at least 2 players.")

        # Remove existing player entry fields if any
        for widget in frame_players.winfo_children():
            widget.destroy()

        # Create player entry fields for names
        tk.Label(frame_players, text="Enter Player Names:").grid(
            row=0, column=0, columnspan=2
        )

        for i in range(num_players):
            tk.Label(frame_players, text=f"Player {i + 1}:").grid(row=i + 1, column=0)
            entry_player_name = tk.Entry(frame_players)
            entry_player_name.grid(row=i + 1, column=1)
            players.append(entry_player_name)

        # Create a single button to save all player names
        btn_save = tk.Button(
            frame_players, text="Save Player Names", command=save_player_info
        )
        btn_save.grid(row=num_players + 1, column=0, columnspan=2)

    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number of players.")


# Function to save player names and collapse the player entry section
def save_player_info():
    global players
    for entry in players:
        player_name = entry.get().strip()
        if player_name:
            scores[player_name] = {
                "bid_input": None,
                "tricks_input": None,
                "round_score": 0,
                "total_score": 0,
                "display_name": player_name,
                "bid": 0,
                "tricks": 0,
            }
            bags[player_name] = 0  # Initialize bags
        else:
            messagebox.showwarning("Input Warning", "Player name cannot be empty.")

    # Remove or collapse player name entry section
    frame_players.grid_remove()  # Hide the player name entry frame
    setup_bids_tricks()  # Proceed to setup bids and tricks


# Function to create fields for bids and tricks
def setup_bids_tricks():
    global current_round
    # Remove existing bid and trick entry fields if any
    for widget in frame_bids.winfo_children():
        widget.destroy()

    # Display the current round number
    tk.Label(frame_bids, text=f"Round {current_round} Bids and Tricks:").grid(
        row=0, column=0, columnspan=4
    )

    for i, player_entry in enumerate(players):
        player_name_str = player_entry.get().strip()  # Get the player's name
        tk.Label(frame_bids, text=f"{player_name_str} Bid:").grid(row=i + 1, column=0)
        bid_entry = tk.Entry(frame_bids)
        bid_entry.grid(row=i + 1, column=1)
        scores[player_name_str][
            "bid_input"
        ] = bid_entry  # Store reference to the bid entry

        tk.Label(frame_bids, text=f"{player_name_str} Tricks:").grid(
            row=i + 1, column=2
        )
        tricks_entry = tk.Entry(frame_bids)
        tricks_entry.grid(row=i + 1, column=3)
        scores[player_name_str][
            "tricks_input"
        ] = tricks_entry  # Store reference to the tricks entry

    # Button to calculate scores
    global btn_calculate
    btn_calculate = tk.Button(
        frame_bids, text="Calculate Scores", command=calculate_score
    )
    btn_calculate.grid(row=len(players) + 1, column=0, columnspan=4)

    # Button to proceed to the next round
    global btn_next_round
    btn_next_round = tk.Button(
        frame_bids, text="Next Round", command=next_round, state=tk.DISABLED
    )
    btn_next_round.grid(row=len(players) + 2, column=0, columnspan=4)


# Function to create a final PDF at the end of the game
def create_final_pdf():
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    elements = []

    final_scores = [["Player", "Total Score", "Bags"]]
    for player_name in scores:
        final_scores.append(
            [
                scores[player_name]["display_name"],
                scores[player_name]["total_score"],
                bags[player_name],
            ]
        )

    final_table = Table(final_scores)
    style = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ]
    )

    final_table.setStyle(style)

    elements.append(Table([["Final Scores After 13 Rounds"]], colWidths=[400]))
    elements.append(Table([[""]]))  # Add space before the final scores
    elements.append(final_table)

    # Build the final PDF
    doc.build(elements)


# Main application setup
root = tk.Tk()
root.title("Spades Score Tracker")

# Entry for number of players
tk.Label(root, text="Number of Players:").grid(row=0, column=0)
entry_num_players = tk.Entry(root)
entry_num_players.grid(row=0, column=1)

# Button to setup players
btn_setup_players = tk.Button(root, text="Setup Players", command=setup_players)
btn_setup_players.grid(row=0, column=2)

# Frame for player inputs (names)
frame_players = tk.Frame(root)
frame_players.grid(row=1, column=0, columnspan=3)

# Frame for bids and tricks
frame_bids = tk.Frame(root)
frame_bids.grid(row=2, column=0, columnspan=4)

# Label to display results
lbl_result = tk.Label(root, text="")
lbl_result.grid(row=3, column=0, columnspan=4)

# Run the Tkinter event loop
root.mainloop()
