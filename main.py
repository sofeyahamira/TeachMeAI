import json
from difflib import get_close_matches

# load the knowledge base
def load_knowledge_base(file_path: str) -> dict:
  with open(file_path, "r") as file:
    data : dict = json.load(file)
  return data

# save to knowlegde base
def save_knowledge_base(file_path : str, data : dict):
  with open(file_path, "w") as file:
    json.dump(data, file, indent=2)

# find the best responses from the dictionary
def find_best_matches(user_questions : str, questions : list[str]) -> str | None:
  matches: list = get_close_matches(user_questions, questions, n=1, cutoff=0.6)
  return matches[0] if matches else None

# get answer
def get_answer_for_question(question : str, knowledge_base : dict) -> str | None:
  for q in knowledge_base["questions"]:
    if q["question"] == question:
      return q["answer"]

# the actual chat bot
def chat_bot():
  knowledge_base : dict = load_knowledge_base('knowledge_base.json')

  #infinite loop
  while True:
    user_input : str = input("You: ")
    if user_input.lower() == 'quit':
      break

    # looking for the best match
    best_match : str | None = find_best_matches(user_input, [q["question"] for q in knowledge_base["questions"]])

    # getting the answer
    if best_match:
      answer = get_answer_for_question(best_match, knowledge_base)
      print(f"Bot: {answer}")
    # if it's a new question
    else:
      print("Bot: I don't know the answer, can you teach me?")
      # getting the new answer
      new_answer : str = input("You: ")
      # adding the new question & answer
      knowledge_base["questions"].append({"question" : user_input, "answer" : new_answer})
      save_knowledge_base("knowledge_base.json", knowledge_base)
      print("Bot: Thank you for teaching me.")

# starting
if __name__ == '__main__':
  chat_bot()
