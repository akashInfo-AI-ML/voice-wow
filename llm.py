import google.genai as genai
import config

client = genai.Client(api_key=config.GEMINI_FREE_API)
chat = client.chats.create(model="gemini-2.5-flash")

BNF_LIMIT = 5
count = 0


def ask_llm(response, question):
    global count
    count += 1
    
    # Handle the ending after BNF_LIMIT questions
    if count == BNF_LIMIT:
        # Send the ending prompt to gracefully conclude
        ending_prompt = ending_prompt = """System: Conclude the interview with a brief, concise response (2-3 sentences max): acknowledge their answer, thank them, mention next steps, and end professionally. Keep it short and positive."""
        
        qn = chat.send_message(ending_prompt)
        return qn, True
    
    # Build context from chat history
    context = ""
    for message in chat.get_history():
        context += f"role - {message.role}: {message.parts[0].text}\n"
    
    # Handle None response from candidate
    if response is not None and response.strip():
        context += f"role - user: {response}\n"
    elif count > 1:  # If it's not the first question and response is None
        context += f"role - user: [No response provided]\n"
        context += f"role - system: The candidate didn't provide an answer. Move to the next question or conclude if this is the final question.\n"
    
    if question:
        context += f"role - system: {question}\n"
    
    # Get response from the chat
    try:
        qn = chat.send_message(context).candidates[0].content.parts[0].text

        if count >= BNF_LIMIT:
            return qn, True
        
        # Handle None or empty response
        if qn is None or not qn.strip():
            qn = chat.send_message(context + "system: Move on to the next question.\n").candidates[0].content.parts[0].text
            # if count < BNF_LIMIT:
            # else:
            #     qn = chat.send_message(context + "system: Please provide the closing response as instructed.\n").candidates[0].content.parts[0].text
            #     print('here1')
            #     return qn, True
            
            # If still None after fallback
            if qn is None:
                qn = "Let me move to the next question."
                # if count < BNF_LIMIT:
                # else:
                #     qn = "Thank you for taking the time to interview with us today. We'll be in touch soon!"
                #     print('here2')
                #     return qn, True
                
    except Exception as e:
        # Error handling
        qn = "I apologize for the technical difficulty. Let me move to the next question."
        # if count < BNF_LIMIT:
        # else:
        #     qn = "Thank you for taking the time to interview with us today. We appreciate your thoughtful responses and will be in touch soon regarding next steps. Have a great day!"
        #     print('here3')
        #     return qn, True
    
    print('here4')
    return qn, False