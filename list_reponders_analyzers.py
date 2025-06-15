import requests
import json
import sys
import urllib3
from dotenv import load_dotenv
import os

load_dotenv()

# Configuration - Update these values with your actual credentials
THE_HIVE_URL = os.getenv("THEHIVE_URL", "http://localhost:9000/api")  # Replace with your TheHive URL
THE_HIVE_API_KEY = os.getenv("THEHIVE_API_KEY", "your_api_key_here") # Replace with your API key

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def list_all_analyzers(api_url, api_key):
    """
    Get a list of all available Cortex analyzers
    
    Args:
        api_url (str): TheHive API URL
        api_key (str): TheHive API key
    """
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    # Ensure the URL has the correct format
    if api_url.endswith('/'):
        api_url = api_url[:-1]
    
    url = f"{api_url}/connector/cortex/analyzer"
    
    try:
        response = requests.get(url, headers=headers, verify=False)
        
        if response.status_code == 200:
            analyzers = response.json()
            
            print(f"\n=== {len(analyzers)} AVAILABLE CORTEX ANALYZERS ===")
            
            # Group analyzers by Cortex instance
            analyzers_by_cortex = {}
            for analyzer in analyzers:
                cortex_id = analyzer.get('cortexId', 'Unknown')
                if cortex_id not in analyzers_by_cortex:
                    analyzers_by_cortex[cortex_id] = []
                analyzers_by_cortex[cortex_id].append(analyzer)
            
            # Display analyzers grouped by Cortex instance
            for cortex_id, cortex_analyzers in analyzers_by_cortex.items():
                print(f"\n== Cortex Instance: {cortex_id} ==")
                
                # Sort analyzers by name
                cortex_analyzers.sort(key=lambda x: x.get('name', '').lower())
                
                for analyzer in cortex_analyzers:
                    print(f"- {analyzer.get('name', 'Unknown')} (ID: {analyzer.get('id', 'N/A')})")
                    data_types = analyzer.get('dataTypeList', [])
                    print(f"  Supported data types: {', '.join(data_types)}")
        else:
            print(f"Error getting analyzers: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error connecting to TheHive: {str(e)}")

def list_available_responders(api_url, api_key, entity_type, entity_id):
    """
    List responders available for a specific entity in TheHive
    Supports both 'observable' and 'case_artifact' entity types
    
    Args:
        api_url (str): TheHive API URL base
        api_key (str): TheHive API key
        entity_type (str): Type of entity (case, alert, observable, case_artifact)
        entity_id (str): ID of the entity
    
    Returns:
        list: List of available responders if successful, empty list otherwise
    """
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    # Ensure the URL has the correct format
    if api_url.endswith('/'):
        api_url = api_url[:-1]
    
    # Validate entity type and prepare endpoints
    valid_entity_types = ['case', 'alert', 'observable', 'case_artifact']
    if entity_type.lower() not in valid_entity_types:
        print(f"Error: Entity type must be one of {valid_entity_types}")
        return []
    
    # For observables, try multiple endpoint formats
    if entity_type.lower() in ['observable', 'case_artifact']:
        endpoints = [
            f"/connector/cortex/responder/case_artifact/{entity_id}",  # Older format
            f"/v1/connector/cortex/responder/case_artifact/{entity_id}",  # v1 API older format
            f"/connector/cortex/responder/observable/{entity_id}",  # Newer format
            f"/v1/connector/cortex/responder/observable/{entity_id}"   # v1 API newer format
        ]
    else:
        endpoints = [
            f"/connector/cortex/responder/{entity_type.lower()}/{entity_id}",
            f"/v1/connector/cortex/responder/{entity_type.lower()}/{entity_id}"
        ]
    
    for endpoint in endpoints:
        url = f"{api_url}{endpoint}"
        print(f"Trying endpoint: {endpoint}")
        
        try:
            response = requests.get(url, headers=headers, verify=False)
            
            if response.status_code == 200:
                responders = response.json()
                print(f"Successfully retrieved {len(responders)} responders from endpoint: {endpoint}")
                return responders
            else:
                print(f"Endpoint {endpoint} returned: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"Error trying endpoint {endpoint}: {str(e)}")
            continue
    
    print(f"Error: Could not get responders for {entity_type} {entity_id} from any endpoint")
    return []

def display_entity_responders(responders):
    """Display available responders for a specific entity"""
    if not responders:
        print("No responders available for this entity.")
        return
    
    print(f"\n=== {len(responders)} AVAILABLE RESPONDERS ===")
    
    # Group responders by Cortex instance
    responders_by_cortex = {}
    for responder in responders:
        cortex_id = responder.get('cortexId', 'Unknown')
        if cortex_id not in responders_by_cortex:
            responders_by_cortex[cortex_id] = []
        responders_by_cortex[cortex_id].append(responder)
    
    # Display responders grouped by Cortex instance
    for cortex_id, cortex_responders in responders_by_cortex.items():
        print(f"\nCortex Instance: {cortex_id}")
        
        # Sort responders by name
        cortex_responders.sort(key=lambda x: x.get('name', '').lower())
        
        for responder in cortex_responders:
            print(f"- {responder.get('name', 'Unknown')} (ID: {responder.get('id', 'N/A')})")
            if 'description' in responder and responder['description']:
                print(f"  Description: {responder.get('description')}")

def main():
    
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  List all analyzers: python cortex_list.py analyzers")
        print("  List entity responders: python cortex_list.py responders <entity_type> <entity_id>")
        print("  Example: python cortex_list.py responders case_artifact 12345")
        return
    
    action = sys.argv[1].lower()
    
    if action == "analyzers":
        list_all_analyzers(THE_HIVE_URL, THE_HIVE_API_KEY)
    elif action == "responders" and len(sys.argv) > 3:
        entity_type = sys.argv[2]
        entity_id = sys.argv[3]
        display_entity_responders(list_available_responders(THE_HIVE_URL, THE_HIVE_API_KEY, entity_type, entity_id))
    else:
        print("Invalid command or missing parameters.")
        print("Use 'analyzers' to list all analyzers")
        print("Use 'responders <entity_type> <entity_id>' to list responders for a specific entity")

if __name__ == "__main__":
    main()