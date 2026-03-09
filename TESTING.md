# Testing Guide

Complete testing checklist for the Context-Aware Personal Executive system.

## 🧪 Test Checklist

### Backend Tests

#### 1. Health Check
```bash
# Test root endpoint
curl http://localhost:8000/

# Expected: {"status":"running","service":"Context-Aware Personal Executive","version":"1.0.0"}
```

#### 2. Stats Endpoint
```bash
curl http://localhost:8000/stats

# Expected: {"documents_indexed":..., "upcoming_events":..., "agent_status":"active"}
```

#### 3. Events Endpoint
```bash
curl http://localhost:8000/events

# Expected: {"events":[{"event":"Logistics Meeting",...}]}
```

#### 4. Ask Endpoint (Reactive Mode)
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d "{\"query\":\"What did we decide about logistics?\"}"

# Expected: {"response":"...", "sources":["Emails"]}
```

#### 5. Check Reminders
```bash
curl http://localhost:8000/check-reminders

# Expected: {"status":"success","reminders":[...],"count":...}
```

### Frontend Tests

#### 1. UI Loading
- [ ] Open http://localhost:5173
- [ ] Page loads without errors
- [ ] Chat interface is visible
- [ ] Reminder panel is visible
- [ ] Initial greeting message appears

#### 2. Chat Functionality
- [ ] Type a message in the input box
- [ ] Click "Send" button
- [ ] Message appears on the right (user message)
- [ ] Response appears on the left (AI message)
- [ ] Loading animation shows while processing

#### 3. Test Queries

**Email Search:**
- [ ] Query: "What did we decide about the logistics?"
- [ ] Expected: Details about venue, transportation, catering

**Calendar Search:**
- [ ] Query: "When is the next meeting?"
- [ ] Expected: Details about upcoming meetings

**PDF Search:**
- [ ] Query: "What is the budget breakdown?"
- [ ] Expected: Budget details from PDF

**CSV Search:**
- [ ] Query: "Show me all events"
- [ ] Expected: List of events from CSV

**Multi-source:**
- [ ] Query: "Tell me everything about the logistics meeting"
- [ ] Expected: Combined information from multiple sources
- [ ] Check "Sources:" shows multiple sources

#### 4. Reminders Panel
- [ ] Right panel shows "Upcoming Events"
- [ ] Events are listed with dates and times
- [ ] Days until event is shown
- [ ] Color coding works (today=red, tomorrow=yellow, future=blue)
- [ ] Active reminders section appears if events within 24h

### Integration Tests

#### 1. End-to-End Flow
```
User Query → Frontend → Backend → Agent → Tools → Response
```

**Steps:**
1. [ ] Open frontend
2. [ ] Ask: "What venue was selected?"
3. [ ] Verify response mentions "City Convention Hall"
4. [ ] Check sources include "Emails"
5. [ ] Response appears within 5 seconds

#### 2. Vector Search Test
1. [ ] Ask: "logistics transportation"
2. [ ] Verify semantic search works
3. [ ] Response should mention buses even if query doesn't say "buses"

#### 3. Calendar Integration Test
1. [ ] Ask: "What's on my calendar?"
2. [ ] Verify events from events.csv appear
3. [ ] Check dates are parsed correctly
4. [ ] Upcoming events show in reminder panel

### n8n Automation Tests

#### 1. Workflow Import
- [ ] n8n is running at http://localhost:5678
- [ ] Import `n8n/reminder_workflow.json`
- [ ] Workflow appears in dashboard
- [ ] All nodes are connected correctly

#### 2. Manual Execution
- [ ] Click "Execute Workflow" in n8n
- [ ] Verify it calls backend endpoint
- [ ] Check if reminders are detected
- [ ] View execution logs

#### 3. Scheduled Execution
- [ ] Activate the workflow
- [ ] Wait for next hour (or change schedule to 5 mins for testing)
- [ ] Check execution history
- [ ] Verify it runs automatically

### Error Handling Tests

#### 1. Backend Errors
- [ ] Stop backend
- [ ] Try to send message in frontend
- [ ] Error message appears: "Please make sure the backend server is running"

#### 2. Invalid API Key
- [ ] Use invalid OpenAI API key
- [ ] Backend should show error message
- [ ] Frontend shows appropriate error

#### 3. Empty Query
- [ ] Try to send empty message
- [ ] Button should be disabled
- [ ] No API call is made

#### 4. Missing Data Files
- [ ] Remove `emails.txt`
- [ ] Query about emails
- [ ] Should return "No email data found"

### Performance Tests

#### 1. Response Time
- [ ] Measure time from query to response
- [ ] Should be < 5 seconds for simple queries
- [ ] Should be < 10 seconds for complex queries

#### 2. Multiple Queries
- [ ] Send 5 queries in a row
- [ ] All should complete successfully
- [ ] No timeout errors

#### 3. Large Context
- [ ] Add more data to files
- [ ] Test performance doesn't degrade significantly

### Data Accuracy Tests

#### 1. Email Search Accuracy
```
Query: "Who is handling catering?"
Expected: "ABC Caterers"
```

#### 2. Date Parsing
```
Query: "When is the logistics meeting?"
Expected: "March 12, 2026 at 10:00"
```

#### 3. Multiple Facts
```
Query: "How many buses are arranged?"
Expected: "Two buses"
```

#### 4. Venue Information
```
Query: "What is the venue address?"
Expected: "123 Main Street, Downtown"
```

## 📊 Test Results Template

```markdown
## Test Run: [Date]

### Environment
- Backend: http://localhost:8000
- Frontend: http://localhost:5173
- Python Version: [version]
- Node Version: [version]

### Results

| Test Category | Pass | Fail | Notes |
|--------------|------|------|-------|
| Backend Health | ✅ | ❌ | |
| Frontend UI | ✅ | ❌ | |
| Email Search | ✅ | ❌ | |
| Calendar Integration | ✅ | ❌ | |
| Vector Search | ✅ | ❌ | |
| Error Handling | ✅ | ❌ | |
| n8n Automation | ✅ | ❌ | |

### Issues Found
1. [Issue description]
2. [Issue description]

### Recommendations
1. [Recommendation]
2. [Recommendation]
```

## 🔍 Debugging Tips

### Check Logs

**Backend Logs:**
Look at the terminal running uvicorn for:
- ✅ "Agent initialized successfully"
- ✅ "Loaded X events from calendar"
- ✅ "Processing query: ..."
- ⚠️ Any error messages

**Frontend Logs:**
Open browser console (F12) and check for:
- Network errors
- JavaScript errors
- API call responses

### Verify Data Files

```bash
# Check data directory
dir backend\data

# View email content
type backend\data\emails.txt

# View events
type backend\data\events.csv
```

### Test API Directly

Use the interactive docs at http://localhost:8000/docs

1. Click on endpoint
2. Click "Try it out"
3. Enter parameters
4. Click "Execute"
5. View response

## ✅ Success Criteria

The system passes all tests when:

- [x] Backend starts without errors
- [x] Frontend loads correctly
- [x] All API endpoints respond
- [x] Chat functionality works
- [x] AI responses are relevant and accurate
- [x] Sources are correctly attributed
- [x] Calendar events display properly
- [x] Reminders are detected correctly
- [x] Error handling works gracefully
- [x] n8n workflow executes successfully

## 🎯 Performance Benchmarks

| Metric | Target | Acceptable | Poor |
|--------|--------|------------|------|
| Page Load | < 1s | < 3s | > 3s |
| Query Response | < 3s | < 8s | > 8s |
| Vector Search | < 2s | < 5s | > 5s |
| API Latency | < 1s | < 2s | > 2s |

## 📝 Test Coverage

- ✅ Unit Tests: Tool functions
- ✅ Integration Tests: API endpoints
- ✅ E2E Tests: Full user flows
- ✅ Error Tests: Edge cases
- ✅ Performance Tests: Response times

---

**Happy Testing! 🎉**

If you find issues, check:
1. Logs in terminal
2. Browser console
3. API docs at /docs
4. README troubleshooting section
