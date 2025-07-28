import json
import os
import time
from dotenv import load_dotenv

from app.smithery import SmithreApi


def main():
    load_dotenv()
    api_key = os.getenv("SMITHERY_API_KEY")
    update_freq = int(os.getenv("SMITHERY_API_KEY")) * 3600
    app = SmithreApi(api_key)
    recheck_time = 72*60*60
    
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
        previous_results["servers"][server_name]["updated_at"] = timestamp # TODO current timestamp(ms)
        
        if index % 20 == 0:
            with open("result.json", "w+") as file:
                json.dump(previous_results, file)
        
        time.sleep(1)
        
        
    with open("result.json", "w+") as file:
        json.dump(previous_results, file)
    
    servers_list_save = [ previous_results["servers"][server_key] for server_key in previous_results["servers"] ]
    
    with open("result_list.json", "w+") as file:
        json.dump(servers_list_save, file)
    

if __name__ == "__main__":
    main()
