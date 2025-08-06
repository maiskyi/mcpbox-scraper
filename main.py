import json
import os
import time
from dotenv import load_dotenv
from google.cloud import storage

from app.smithery import SmithreApi


def main():
    load_dotenv()
    api_key = os.getenv("SMITHERY_API_KEY")
    bucket_name = os.getenv("STORAGE_BACKET_NAME")
    bucket_folder = os.getenv("STORAGE_BACKET_FOLDER")
    storage_account_key = os.getenv("STORAGE_SERVICE_ACCOUNT_KEY")
    update_freq = int(os.getenv("SMITHERY_UPDATE_FREQ")) * 3600
    
    app = SmithreApi(api_key)
    # storage_client = storage.Client.from_service_account_json(storage_account_key)
    storage_client = storage.Client()
    
    if os.path.exists("result.json"):
        with open("result.json", "r") as file:
            previous_results = json.load(file)
    else:
        previous_results = {
            "servers": {}
        }

    servers_list = app.get_all_servers()

    for index, server in enumerate(servers_list):
        timestamp = int(time.time()*1000)
        server_name = server["qualifiedName"]
        print(f"Server {server_name}")
        if server_name not in previous_results["servers"]:
            print("New server")
            previous_results["servers"][server_name] = {
                "title": server["displayName"],
                "description": server["description"]
            }
            server_html_data = app.get_server_data_web(server_name)
            if not server_html_data["exists"]:
                print("Server doesn't exists")
                continue
            previous_results["servers"][server_name]["isOfficial"] = server_html_data["isOfficial"]
            previous_results["servers"][server_name]["githubUrl"] = server_html_data["githubUrl"]
        
        if "updated_at" in previous_results["servers"][server_name] and timestamp -  previous_results["servers"][server_name]["updated_at"] < update_freq * 1000:
            print("Server data actual")
            continue

        server_data = app.get_server_data(server_name)
        if not server_data["exists"]:
            print("Server doesn't exists")
            continue
        
        previous_results["servers"][server_name]["logo"] = server_data["iconUrl"]
        previous_results["servers"][server_name]["tools"] = server_data["tools"]
        previous_results["servers"][server_name]["settings"] = server_data["settings"]
        previous_results["servers"][server_name]["original_api_data"] = server_data
        previous_results["servers"][server_name]["updated_at"] = timestamp
        
        filename = server_name.replace("/", "_")
        destination_file_name = f"{bucket_folder}/{filename}.json"
        blob = storage_client.bucket(bucket_name).blob(destination_file_name)
        blob.upload_from_string(json.dumps(previous_results["servers"][server_name]), content_type='application/json')
        print(f"File uploaded to gs://{bucket_name}/{destination_file_name}")
        
        if index % 20 == 0:
            with open("result.json", "w+") as file:
                json.dump(previous_results, file)
        
        time.sleep(1)
        
    with open("result.json", "w+") as file:
        json.dump(previous_results, file)
    

if __name__ == "__main__":
    main()
