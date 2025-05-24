## Design document

REST API backend to fetch a prompt and score answers

### Endpoints

#### Prompt
GET: generate prompt using openAI API
 - Response: prompt

#### Answer
POST: Submit answer
 - Request body: User-submitted answer
 - Task: Save answer to db, score with GPT-Zero
 - Response: GPT-Zero Score

#### Review
GET:
 - Request body: Answer id
 - Response: ChatGPT feedback

 Data:
 Prompt generated daily using lambda, stored in file

 DB:

 Prompt
  - prompt id
  - prompt
  - date
 
 User
  - user id
  - username
  - password


 Answer:
  - user id
  - prompt id
  - answer id
  - score