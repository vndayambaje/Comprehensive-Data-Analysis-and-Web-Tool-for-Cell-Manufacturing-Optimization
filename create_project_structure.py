import os

def create_directory_structure(base_dir="cell_manufacturing_project"):
    structure = {
        "data": ["generated_data.csv", "processed_data/"],
        "scripts": ["data_generation.py", "data_ingestion.py", "data_processing.py", "root_cause_analysis.py", "web_server/", "web_server/app.py", "web_server/frontend/", "web_server/frontend/src/", "web_server/frontend/src/App.js"],
        "airflow_dags": ["data_pipeline_dag.py"],
    }

    for folder, files in structure.items():
        folder_path = os.path.join(base_dir, folder)
        os.makedirs(folder_path, exist_ok=True)
        for file in files:
            file_path = os.path.join(folder_path, file)
            if "." in file:  # If it's a file
                dir_name = os.path.dirname(file_path)
                os.makedirs(dir_name, exist_ok=True)  # Ensure the directory exists
                with open(file_path, 'w') as f:
                    f.write("")
            else:  # If it's a sub-folder
                os.makedirs(file_path, exist_ok=True)

    # Additional README and requirements.txt
    open(os.path.join(base_dir, "README.md"), 'w').close()
    open(os.path.join(base_dir, "requirements.txt"), 'w').close()

    print(f"Project structure created under '{base_dir}'")

if __name__ == "__main__":
    create_directory_structure()
