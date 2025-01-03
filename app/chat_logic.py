import json
from pathlib import Path
import re
from difflib import SequenceMatcher

class ChatBot:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent.parent
        self.load_knowledge_base()
    
    def load_knowledge_base(self):
        faq_path = self.base_dir / 'data' / 'EcoNest_FAQs.json'
        scenario_path = self.base_dir / 'data' / 'EcoNest_Customer_Support_Scenarios.json'
        
        with open(faq_path, 'r') as f:
            self.faqs = json.load(f)['faqs']
        
        with open(scenario_path, 'r') as f:
            self.scenarios = json.load(f)['scenarios']
        
        self.qa_pairs = []
        self.qa_pairs.extend([(qa['question'], qa['answer']) for qa in self.faqs])
        self.qa_pairs.extend([(s['customer_query'], s['response']) for s in self.scenarios])

    def get_response(self, user_input: str) -> str:
        user_input = user_input.lower().strip()
        
        best_match = None
        highest_score = 0
        similar_questions = []
        
        # First try exact matching
        for question, answer in self.qa_pairs:
            if user_input == question.lower().strip():
                return answer
                
            # Calculate similarity
            score = self.calculate_similarity(user_input, question.lower())
            
            if score > highest_score:
                highest_score = score
                best_match = answer
                
            if score > 0.5:  # Keep track of similar questions
                similar_questions.append((question, score))
        
        # If we have a good match, return it
        if highest_score > 0.6:
            return best_match
            
        # If we have similar questions but no great match, suggest them
        if similar_questions:
            sorted_similar = sorted(similar_questions, key=lambda x: x[1], reverse=True)[:3]
            suggestion_text = "\n\nDid you mean one of these?\n- " + "\n- ".join(q[0] for q in sorted_similar)
            return f"I'm not quite sure about that.{suggestion_text}\n\nOr you can contact our support team at support@econestco.com for more detailed assistance."
            
        return "I apologize, but I'm not sure about that. Could you please rephrase your question or contact our support team at support@econestco.com for more detailed assistance?"

    def calculate_similarity(self, input1: str, input2: str) -> float:
        # Using sequence matcher for better fuzzy matching
        return SequenceMatcher(None, input1, input2).ratio()
