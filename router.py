import os
import json
import logging
from typing import Dict, Any
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Logging
LOG_FILE = "route_log.jsonl"
logging.basicConfig(level=logging.INFO)

# Initialize LLM
# Note: Using Gemini as the LLM provider
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-flash-latest')

def load_prompts() -> Dict[str, Any]:
    with open("prompts.json", "r") as f:
        return json.load(f)

def log_request(intent: str, confidence: float, message: str, response: str):
    log_entry = {
        "intent": intent,
        "confidence": confidence,
        "user_message": message,
        "final_response": response
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

def classify_intent(message: str) -> Dict[str, Any]:
    prompts = load_prompts()
    system_prompt = prompts["classifier"]["system_prompt"]
    
    try:
        # Prompt construction
        full_prompt = f"{system_prompt}\n\nUser Message: {message}"
        
        response = model.generate_content(
            full_prompt,
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json",
            )
        )
        
        # Parse response
        try:
            result = json.loads(response.text)
            # Ensure keys exist
            if "intent" not in result or "confidence" not in result:
                raise ValueError("Missing keys in LLM response")
            return result
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error parsing LLM response: {e}. Raw response: {response.text}")
            return {"intent": "unclear", "confidence": 0.0}
            
    except Exception as e:
        print(f"Error during classification call: {e}")
        return {"intent": "unclear", "confidence": 0.0}

def route_and_respond(message: str, classification: Dict[str, Any]) -> str:
    prompts = load_prompts()
    intent = classification.get("intent", "unclear")
    confidence = classification.get("confidence", 0.0)
    
    # Confidence threshold (Optional stretch goal)
    if confidence < 0.7:
        intent = "unclear"

    if intent == "unclear" or intent not in prompts["experts"]:
        response_text = prompts["clarification"]
    else:
        expert_prompt = prompts["experts"][intent]
        try:
            full_prompt = f"{expert_prompt}\n\nUser Message: {message}"
            response = model.generate_content(full_prompt)
            response_text = response.text
        except Exception as e:
            print(f"Error during expert generation call: {e}")
            response_text = "I encountered an error while trying to process your request."

    # Log the interaction
    log_request(intent, confidence, message, response_text)
    
    return response_text

if __name__ == "__main__":
    # Quick sanity check
    test_msg = "how do i sort a list in python?"
    print(f"Testing with: {test_msg}")
    intent_data = classify_intent(test_msg)
    print(f"Classified as: {intent_data}")
    final_resp = route_and_respond(test_msg, intent_data)
    print(f"Final Response: {final_resp}")
