import os

# Define the paths to the stored metadata and FAISS index
metadata_path = r'C:\Users\AbhinavKasubojula\OneDrive - Kenall Inc\Desktop\code\stored_data\faiss_index.bin'
faiss_index_path = r'C:\Users\AbhinavKasubojula\OneDrive - Kenall Inc\Desktop\code\stored_data\metadata.pkl'

def clear_stored_data():
    # Check if metadata file exists and delete it
    if os.path.exists(metadata_path):
        os.remove(metadata_path)
        print(f"Deleted: {metadata_path}")
    else:
        print(f"{metadata_path} not found!")

    # Check if FAISS index file exists and delete it
    if os.path.exists(faiss_index_path):
        os.remove(faiss_index_path)
        print(f"Deleted: {faiss_index_path}")
    else:
        print(f"{faiss_index_path} not found!")


# Call the function to clear stored data
clear_stored_data()
