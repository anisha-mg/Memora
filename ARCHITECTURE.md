# System Architecture

Detailed architecture documentation for the Context-Aware Personal Executive system.

## 🏛️ High-Level Architecture

```
┌─────────────────────────────────────────────────────┐
│                    User Interface                    │
│                  (React + Vite)                      │
│  ┌──────────────┐              ┌─────────────────┐ │
│  │  Chat Box    │              │ Reminder Panel  │ │
│  │  Component   │              │   Component     │ │
│  └──────────────┘              └─────────────────┘ │
└────────────────────┬────────────────────────────────┘
                     │ HTTP/REST API
                     ▼
┌─────────────────────────────────────────────────────┐
│               FastAPI Backend                        │
│  ┌─────────────────────────────────────────────┐   │
│  │          Context-Aware Agent                │   │
│  │         (OpenAI + LangChain)                │   │
│  │                                              │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  │   │
│  │  │ Decision │→ │   Tool   │→ │ Response │  │   │
│  │  │  Engine  │  │ Executor │  │Generator │  │   │
│  │  └──────────┘  └──────────┘  └──────────┘  │   │
│  └─────────────────────────────────────────────┘   │
│                     │                               │
│        ┌────────────┼────────────┐                  │
│        ▼            ▼            ▼                  │
│  ┌─────────┐  ┌─────────┐  ┌──────────┐           │
│  │  Email  │  │   PDF   │  │ Calendar │           │
│  │  Tool   │  │  Tool   │  │  Service │           │
│  └─────────┘  └─────────┘  └──────────┘           │
│        │            │            │                  │
│        └────────────┼────────────┘                  │
│                     ▼                               │
│          ┌──────────────────────┐                  │
│          │   FAISS Vector DB    │                  │
│          │  (Semantic Search)   │                  │
│          └──────────────────────┘                  │
└─────────────────────────────────────────────────────┘
                     │
                     ▼
         ┌──────────────────────┐
         │    Data Layer        │
         │  • emails.txt        │
         │  • notes.pdf         │
         │  • events.csv        │
         └──────────────────────┘

    ┌────────────────────────────┐
    │     n8n Automation         │
    │  (Proactive Reminders)     │
    │                            │
    │  Schedule → Check → Notify │
    └────────────────────────────┘
```

## 📦 Component Details

### 1. Frontend Layer (React + Vite)

#### Components
```
src/
├── components/
│   ├── ChatBox.jsx          # Main chat interface
│   │   ├── Message input
│   │   ├── Message display
│   │   └── Send button
│   │
│   ├── MessageBubble.jsx    # Individual message rendering
│   │   ├── User messages (right, blue)
│   │   ├── AI messages (left, gray)
│   │   └── Source attribution
│   │
│   └── ReminderPanel.jsx    # Event & reminder display
│       ├── Active reminders (yellow)
│       ├── Upcoming events list
│       └── Stats footer
│
├── pages/
│   └── Dashboard.jsx        # Main layout
│       ├── Header
│       ├── Grid layout (2/3 + 1/3)
│       └── Footer
│
└── services/
    └── api.js               # API client
        ├── HTTP client (Axios)
        ├── Endpoint wrappers
        └── Error handling
```

#### State Management
- **Local State**: React useState hooks
- **No Global State**: Simple component-to-component communication
- **Data Flow**: Unidirectional (top-down)

#### Styling
- **Tailwind CSS**: Utility-first CSS framework
- **Responsive**: Mobile-friendly grid layout
- **Animations**: Pulse, fade, transitions

### 2. Backend Layer (FastAPI + Python)

#### Core Modules

**main.py** - API Server
```python
FastAPI Application
├── CORS Middleware
├── Startup Event (initialize services)
└── Endpoints:
    ├── POST /ask         # Query processing
    ├── GET /events       # Calendar events
    ├── POST /reminder    # Create reminder
    ├── GET /check-reminders  # Proactive check
    └── GET /stats        # System statistics
```

**agent.py** - LangChain Agent
```python
ContextAwareAgent
├── OpenAI Client
├── Tool Definitions
├── Query Processor
│   ├── Vector search preprocessing
│   ├── OpenAI function calling
│   ├── Tool execution
│   └── Response synthesis
└── Source Attribution
```

**tools.py** - Data Access Tools
```python
DataTools
├── search_email(query)
│   ├── Load emails.txt
│   ├── Keyword matching
│   └── Return relevant content
│
├── search_pdf(query)
│   ├── Read PDF with PyPDF2
│   ├── Extract text
│   └── Search paragraphs
│
├── search_csv(query)
│   ├── Load CSV with Pandas
│   ├── Search all columns
│   └── Return matching rows
│
└── get_calendar_events()
    ├── Load events.csv
    ├── Filter by date range
    └── Format output
```

**vector_store.py** - FAISS Vector Database
```python
VectorStore
├── Document Loading
│   ├── Load from emails.txt
│   ├── Load from notes.pdf
│   └── Load from events.csv
│
├── Embedding Creation
│   ├── OpenAI Embeddings API
│   └── text-embedding-3-small model
│
├── FAISS Index
│   ├── IndexFlatL2 (L2 distance)
│   └── Similarity search
│
└── Fallback Search
    └── Keyword-based (if FAISS fails)
```

**calendar_service.py** - Calendar Management
```python
CalendarService
├── Load Events (from CSV)
├── Get Upcoming Events
│   └── Filter by date range
│
├── Check Reminders
│   ├── Find events within 24h
│   └── Format reminder messages
│
└── Event Management
    ├── Add events
    └── Update events
```

### 3. AI Agent Design

#### Function Calling Flow

```
User Query: "What did we decide about logistics?"
                    ↓
        ┌───────────────────────┐
        │ OpenAI Chat API       │
        │ with Tool Definitions │
        └───────────┬───────────┘
                    ↓
        ┌───────────────────────┐
        │ Model Analyzes Query  │
        │ Decides: search_email │
        └───────────┬───────────┘
                    ↓
        ┌───────────────────────┐
        │ Execute Tool:         │
        │ search_email("logistics")
        └───────────┬───────────┘
                    ↓
        ┌───────────────────────┐
        │ Tool Returns Results  │
        │ "Venue: City Hall..." │
        └───────────┬───────────┘
                    ↓
        ┌───────────────────────┐
        │ Model Synthesizes     │
        │ Natural Response      │
        └───────────┬───────────┘
                    ↓
        ┌───────────────────────┐
        │ Return to User        │
        │ with Sources          │
        └───────────────────────┘
```

#### Tool Selection Logic

The OpenAI model automatically decides which tool to use based on:

1. **Query Intent**: What is the user asking for?
2. **Tool Descriptions**: Which tool best matches the intent?
3. **Parameters**: What parameters does the tool need?
4. **Context**: Previous conversation history

**Example Tool Mappings:**

| Query Type | Detected Intent | Selected Tool |
|------------|----------------|---------------|
| "What did we decide..." | Past communication | search_email |
| "What's in the notes..." | Document search | search_pdf |
| "Show me the data..." | Structured data | search_csv |
| "When is the meeting..." | Calendar/schedule | get_calendar_events |
| "Remind me about..." | Create reminder | send_reminder |

### 4. Data Flow

#### Reactive Mode (User Query)

```
1. User types query in frontend
   ↓
2. Frontend sends POST /ask
   ↓
3. Backend receives query
   ↓
4. Agent preprocesses with vector search
   ↓
5. Agent calls OpenAI with query + tool definitions
   ↓
6. OpenAI decides which tool(s) to use
   ↓
7. Backend executes selected tool(s)
   ↓
8. Tool returns results
   ↓
9. Agent feeds results back to OpenAI
   ↓
10. OpenAI generates natural language response
    ↓
11. Backend returns response + sources
    ↓
12. Frontend displays in chat
```

#### Proactive Mode (Automated Reminders)

```
1. n8n schedule triggers (every hour)
   ↓
2. n8n calls GET /check-reminders
   ↓
3. Backend checks calendar events
   ↓
4. Filter events within 24 hours
   ↓
5. Format reminder messages
   ↓
6. Return list of reminders
   ↓
7. n8n processes each reminder
   ↓
8. n8n calls POST /reminder for each
   ↓
9. Backend logs reminder
   ↓
10. Reminder appears in frontend panel
```

### 5. Database Design

#### FAISS Vector Database

**Structure:**
```
documents[] = [
  {
    "content": "Email text...",
    "source": "emails",
    "type": "email"
  },
  ...
]

embeddings[] = [
  [0.123, 0.456, ...],  # 1536-dim vector
  ...
]

index = FAISS.IndexFlatL2(1536)
index.add(embeddings)
```

**Search Process:**
```
1. User query → Embedding
2. FAISS finds K nearest neighbors
3. Return top K documents
4. LLM uses for context
```

#### CSV Data Structure

**events.csv:**
```
event,date,time
Logistics Meeting,2026-03-12,10:00
Team Review,2026-03-15,14:00
```

**Loaded as:**
```python
DataFrame with columns: ['event', 'date', 'time']
date column parsed as datetime
```

### 6. API Design

#### RESTful Endpoints

**POST /ask**
- Purpose: Process user query
- Input: `{"query": "string"}`
- Output: `{"response": "string", "sources": []}`
- Processing: Agent → Tools → LLM → Response

**GET /events**
- Purpose: Get upcoming events
- Input: None (query params possible)
- Output: `{"events": [...]}`
- Processing: CalendarService → Filter → Format

**POST /reminder**
- Purpose: Create reminder
- Input: `{"event_name": "...", "event_date": "...", ...}`
- Output: `{"status": "success", "reminder": {...}}`
- Processing: Format message → Store/Log

**GET /check-reminders**
- Purpose: Check for upcoming reminders
- Input: None
- Output: `{"reminders": [...], "count": N}`
- Processing: Filter events within 24h → Format

### 7. Authentication & Security

**Current Implementation:**
- No authentication (demo/local use)
- CORS configured for localhost only
- API key stored in backend .env (not exposed)

**Production Considerations:**
- Add JWT authentication
- Implement rate limiting
- Use OAuth for calendar integration
- Encrypt sensitive data
- Add HTTPS

### 8. Scalability Considerations

#### Current Limitations
- Single instance (no load balancing)
- In-memory vector store (not persistent)
- CSV-based calendar (not scalable)
- No caching layer

#### Scaling Strategy
```
┌──────────────┐
│ Load Balancer│
└───────┬──────┘
        │
   ┌────┴────┐
   ▼         ▼
┌──────┐  ┌──────┐
│API 1 │  │API 2 │
└───┬──┘  └───┬──┘
    └─────┬───┘
          ▼
    ┌──────────┐
    │  Redis   │ (Cache)
    └──────────┘
          │
          ▼
    ┌──────────┐
    │Persistent│
    │Vector DB │ (Pinecone/Weaviate)
    └──────────┘
```

### 9. Error Handling

#### Frontend
- Network errors → User-friendly message
- Timeout → Suggest checking backend
- Empty response → Show default message

#### Backend
- Tool execution errors → Fallback response
- OpenAI API errors → Log and retry
- Missing data → Return "not found" message
- Invalid input → 422 validation error

### 10. Performance Optimization

**Current Optimizations:**
- Lazy loading of documents
- Batch embedding creation
- Caching of vector store
- Chunked document processing

**Further Optimizations:**
- Redis for session caching
- Connection pooling for DB
- CDN for frontend assets
- Async processing for heavy tasks

## 🔄 System Flow Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    User Action                          │
│              (Type query or view reminders)             │
└────────────────────────┬────────────────────────────────┘
                         │
          ┌──────────────┴──────────────┐
          │                             │
    Ask Question                   View Reminders
          │                             │
          ▼                             ▼
    ┌──────────┐                 ┌──────────┐
    │ POST /ask│                 │GET /events│
    └─────┬────┘                 └─────┬────┘
          │                            │
          ▼                            │
    ┌──────────────┐                  │
    │ Agent Process│                  │
    └─────┬────────┘                  │
          │                            │
    ┌─────┴────┐                      │
    │ Tools    │                      │
    └─────┬────┘                      │
          │                            │
          ▼                            ▼
    ┌────────────────────────────────────┐
    │         Data Sources               │
    │  emails.txt | notes.pdf | events.csv
    └────────────┬───────────────────────┘
                 │
                 ▼
         ┌──────────────┐
         │  Response    │
         └──────┬───────┘
                │
                ▼
         ┌──────────────┐
         │   Frontend   │
         │   Display    │
         └──────────────┘
```

---

## 📚 Technology Stack Details

### Frontend
- **React 18**: Component-based UI
- **Vite**: Fast build tool
- **Tailwind**: Utility CSS
- **Axios**: HTTP client

### Backend
- **FastAPI**: Modern Python web framework
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation

### AI/ML
- **OpenAI API**: GPT-4o-mini
- **LangChain**: Agent orchestration
- **FAISS**: Vector similarity search

### Data Processing
- **PyPDF2**: PDF parsing
- **Pandas**: CSV/data manipulation
- **NumPy**: Numerical operations

---

**This architecture enables:**
- ✅ Fast response times (< 5s)
- ✅ Multi-source search
- ✅ Intelligent tool selection
- ✅ Semantic understanding
- ✅ Automated workflows
- ✅ Extensible design
