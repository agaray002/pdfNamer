import os
import json
import shutil
import re

# Toggle settings
bs_year = "2024"  # Set to the year you want, or leave "" for no year

# Save last-used client and path
config_file = "client_config.json"

def load_last_used():
    if os.path.exists(config_file):
        with open(config_file, "r") as file:
            config = json.load(file)
            return config.get("client_name", ""), config.get("last_folder", "")
    return "", ""

def save_last_used(client_name, folder_path):
    with open(config_file, "w") as file:
        json.dump({"client_name": client_name, "last_folder": folder_path}, file)

def clean_client_name(client_name):
    client_name = client_name.strip()
    client_name = re.sub(r"[-.]+$", "", client_name)  # Remove hyphens and periods at the end
    client_name = re.sub(r"\s*&\s*", "&", client_name)  # Replace " & " with "&"
    client_name = client_name.replace(" ", "_")
    client_name = "".join(char for char in client_name if char.isalnum() or char in ["_", "&", "-", "."])
    return client_name

def main():
    # Load last-used client and folder
    last_client, last_folder = load_last_used()

    print("Welcome to the PDF Renaming Script!")
    client_name = input(f"Enter client name (last used: {last_client}): ").strip() or last_client
    client_name = clean_client_name(client_name)
    print(f"Cleaned Client Name: {client_name}")

    folder_path = input(f"Enter the folder path (last used: {last_folder}): ").strip() or last_folder

    if not os.path.exists(folder_path):
        print("Folder does not exist. Please check the path.")
        return

    save_last_used(client_name, folder_path)

    client_folder = os.path.join(folder_path, client_name.title().replace("_", " "))
    os.makedirs(client_folder, exist_ok=True)

    pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")]

    receipt_files = [f for f in pdf_files if re.match(r"^[a-zA-Z0-9-_&]+(\.pdf)$", f) and not f.lower().startswith("account-statement")]
    statement_files = [f for f in pdf_files if f.lower().startswith("account-statement")]

    # Process Receipts
    for file in receipt_files:
        print(f"Processing Receipt: {file}")
        original_path = os.path.join(folder_path, file)
        x_value = "" if len(receipt_files) == 1 else input("Enter 'x' value for this receipt: ").strip()
        new_filename = f"{client_name}_{x_value}{bs_year}receipt.pdf".replace("__", "_")
        shutil.move(original_path, os.path.join(client_folder, new_filename))

    # Process Statements
    for i, file in enumerate(statement_files, 1):
        print(f"Processing Statement: {file}")
        original_path = os.path.join(folder_path, file)
        x_value = "" if len(statement_files) == 1 else input("Enter 'x' value for this statement: ").strip()
        new_filename = f"{client_name}_{x_value}_account-statement{bs_year}.pdf".replace("__", "_")
        shutil.move(original_path, os.path.join(client_folder, new_filename))

    print(f"\n✅ All files processed and moved to '{client_folder}'")

if __name__ == "__main__":
    main()
