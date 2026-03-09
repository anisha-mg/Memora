"""
Context-Aware AI Agent with LangChain and OpenAI
"""
import os
import json
from typing import Dict, List, Any
from openai import OpenAI
from tools import DataTools, get_tool_definitions


class ContextAwareAgent:
    """
    AI Agent that uses OpenAI function calling to decide which tools to use
    """
    
    def __init__(self, vector_store, calendar_service):
        """
        Initialize the agent
        
        Args:
            vector_store: VectorStore instance for semantic search
            calendar_service: CalendarService instance
        """
        # Initialize OpenAI client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("⚠️  WARNING: OPENAI_API_KEY not set. AI features will not work.")
            print("📝 Add your OpenAI API key to backend/.env file")
            self.client = None
        else:
            self.client = OpenAI(api_key=api_key)
        
        self.model = "gpt-4o-mini"  # or "gpt-3.5-turbo" for faster/cheaper responses
        
        # Initialize tools
        self.data_tools = DataTools()
        self.vector_store = vector_store
        self.calendar_service = calendar_service
        
        # Get tool definitions
        self.tools = get_tool_definitions()
        
        print("✅ Context-Aware Agent initialized with OpenAI")
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """
        Process a user query and return a response
        
        Args:
            query: User's natural language query
            
        Returns:
            Dictionary with 'answer' and 'sources'
        """
        if not self.client:
            return {
                "answer": "⚠️ AI features are disabled. Please add your OpenAI API key to backend/.env file (OPENAI_API_KEY=sk-xxx)",
                "sources": []
            }
        
        try:
            # First, check if we should use vector search
            vector_result = self._try_vector_search(query)
            
            # Prepare messages
            messages = [
                {
                    "role": "system",
                    "content": """You are a helpful personal executive assistant. You have access to various tools to help answer questions:
                    
- search_email: Search through emails
- search_pdf: Search through PDF documents
- search_csv: Search through CSV data
- get_calendar_events: Get upcoming calendar events
- send_reminder: Create reminder notifications

When answering questions:
1. Use the appropriate tool(s) to find information
2. Provide clear, concise answers
3. If relevant information is found in documents, cite it
4. Be proactive and helpful

If vector search results are provided, use them as context."""
                },
                {
                    "role": "user",
                    "content": query
                }
            ]
            
            # Add vector search context if available
            if vector_result:
                messages.insert(1, {
                    "role": "system",
                    "content": f"Relevant context from vector search:\n{vector_result}"
                })
            
            # First API call - let the model decide which tools to use
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=[{
                    "type": "function",
                    "function": tool
                } for tool in self.tools],
                tool_choice="auto"
            )
            
            assistant_message = response.choices[0].message
            tool_calls = assistant_message.tool_calls
            
            # If the model wants to use tools
            if tool_calls:
                # Add assistant's message to conversation
                messages.append({
                    "role": "assistant",
                    "content": assistant_message.content,
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        } for tc in tool_calls
                    ]
                })
                
                # Execute each tool call
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    print(f"🔧 Agent calling tool: {function_name} with args: {function_args}")
                    
                    # Execute the tool
                    function_response = self._execute_tool(function_name, function_args)
                    
                    # Add tool response to messages
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": function_name,
                        "content": function_response
                    })
                
                # Get final response from the model
                final_response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages
                )
                
                final_answer = final_response.choices[0].message.content
            else:
                # No tools needed, use direct response
                final_answer = assistant_message.content
            
            return {
                "answer": final_answer,
                "sources": self._extract_sources(messages)
            }
            
        except Exception as e:
            print(f"❌ Error in agent processing: {str(e)}")
            return {
                "answer": f"I encountered an error processing your request: {str(e)}",
                "sources": []
            }
    
    def _execute_tool(self, function_name: str, function_args: Dict) -> str:
        """
        Execute a tool function
        
        Args:
            function_name: Name of the function to execute
            function_args: Arguments for the function
            
        Returns:
            Tool execution result
        """
        try:
            if function_name == "search_email":
                return self.data_tools.search_email(function_args["query"])
            
            elif function_name == "search_pdf":
                return self.data_tools.search_pdf(function_args["query"])
            
            elif function_name == "search_csv":
                return self.data_tools.search_csv(function_args["query"])
            
            elif function_name == "get_calendar_events":
                days_ahead = function_args.get("days_ahead", 7)
                return self.data_tools.get_calendar_events(days_ahead)
            
            elif function_name == "send_reminder":
                return self.data_tools.send_reminder(
                    event_name=function_args["event_name"],
                    event_date=function_args["event_date"],
                    event_time=function_args["event_time"],
                    details=function_args.get("details", "")
                )
            
            else:
                return f"Unknown function: {function_name}"
                
        except Exception as e:
            return f"Error executing {function_name}: {str(e)}"
    
    def _try_vector_search(self, query: str) -> str:
        """
        Try to find relevant information using vector search
        
        Args:
            query: User query
            
        Returns:
            Relevant documents or empty string
        """
        try:
            if self.vector_store:
                results = self.vector_store.search(query, top_k=3)
                if results:
                    return "\n\n".join([doc["content"] for doc in results])
        except Exception as e:
            error_msg = str(e)
            if "insufficient_quota" in error_msg or "429" in error_msg:
                print(f"⚠️  Vector search skipped (OpenAI quota exceeded)")
            else:
                print(f"⚠️  Vector search failed: {str(e)}")
        
        return ""
    
    def _extract_sources(self, messages: List[Dict]) -> List[str]:
        """
        Extract sources from tool calls in the conversation
        
        Args:
            messages: Conversation messages
            
        Returns:
            List of source names
        """
        sources = []
        for msg in messages:
            if msg.get("role") == "tool":
                tool_name = msg.get("name", "")
                if "email" in tool_name:
                    sources.append("Emails")
                elif "pdf" in tool_name:
                    sources.append("PDF Documents")
                elif "csv" in tool_name:
                    sources.append("CSV Data")
                elif "calendar" in tool_name:
                    sources.append("Calendar")
        
        return list(set(sources))  # Remove duplicates
