
import pdfplumber 
import os
import json

def extract_table_data(pdf_path):
    table_list=[]
    tables=[]
    
    with pdfplumber.open(pdf_path) as pdf:
    
        for page in pdf.pages:
            
            tables=page.extract_table()
            table_list.append(tables)
    
    # Prepare the output data
    output_data = []
    
    # Iterate through nested lists
    for section in table_list:
        for entry in section:
            # Extract topic and subtopics
            topic = entry[0] if entry[0] is not None else ""
            subtopics = entry[1]
            
            # If topic is empty, add to previous entry's subtopics
            if not topic and output_data:
                output_data[-1]["Examples of Subtopics that would be\nincluded"] += "\n" + subtopics
            else:
                output_data.append({
                    "Topics": topic,
                    "Examples of Subtopics that would be\nincluded": subtopics
                })
    

    return output_data

def main():
    table_path="topics.pdf"
    if os.path.exists("table_metadata.json"):
       
       print("Table Metadata found in directory. Reading data from it...")
       with open('table_metadata.json' ,'r') as filename:
            table=json.load(filename)
    else:
        print("Table metadata not existing, extracting metadata...")
        
        table = extract_table_data(table_path)

        with open('table_metadata.json' ,'w') as filename:
            json.dump(table, filename, indent=4)


if __name__=="main":
    main()