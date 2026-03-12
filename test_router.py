from router import classify_intent, route_and_respond
import time

test_messages = [
    "how do i sort a list of objects in python?",
    "explain this sql query for me",
    "This paragraph sounds awkward, can you help me fix it?",
    "I'm preparing for a job interview, any tips?",
    "what's the average of these numbers: 12, 45, 23, 67, 34",
    "Help me make this better.",
    "I need to write a function that takes a user id and returns their profile, but also i need help with my resume.",
    "hey",
    "Can you write me a poem about clouds?",
    "Rewrite this sentence to be more professional.",
    "I'm not sure what to do with my career.",
    "what is a pivot table",
    "fxi thsi bug pls: for i in range(10) print(i)",
    "How do I structure a cover letter?",
    "My boss says my writing is too verbose."
]

def run_tests():
    print(f"{'#'*20} STARTING BATCH TESTS {'#'*20}\n")
    for i, msg in enumerate(test_messages[:5], 1):
        print(f"--- Test {i}/{len(test_messages)} ---")
        print(f"User: {msg}")
        
        classification = classify_intent(msg)
        print(f"Intent: {classification['intent']} (Conf: {classification['confidence']})")
        
        response = route_and_respond(msg, classification)
        print(f"Response: {response[:100]}...") # Print first 100 chars
        print("-" * 50)
        
        # Small delay to avoid rate limits (increased to 10s for free tier)
        time.sleep(10)
        
    print(f"\n{'#'*20} TESTS COMPLETE {'#'*20}")
    print("Check route_log.jsonl for full details.")

if __name__ == "__main__":
    run_tests()
