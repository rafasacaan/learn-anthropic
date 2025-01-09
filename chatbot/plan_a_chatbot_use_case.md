# Plan towards using a chatbot


## I. Sure you need one? Why.
Ask yourself why you should use a chatbot.

- High volume of repetitive tasks?
- Need for quick information synthesis
- 24/7 availability requirement?
- Consistent brand voice



## II. Define your ideal chat interaction

Outline a interaction to **define how and when** you expext a customer to interact wiuth the chatbot.

**Example**

- *Customer*: Initiates support chat experience
    - *Bot*: Warmly greets customer and initiates conversation
- *C*: Asks about insurance foer their new electrioc car
    - *B*: Provides relevant info about electric car insurance
- *C*: Asks questions reltaed to unique needs for electric vehicle insurance
    - *B*: Responds with accurate answers and provides links to sources
- *C*: Asks off topic questions unrelated to insurance or cars
    - *B*: Clarifies it does not respond unrelated topics and steers the user back to car insurance
- *C*: Expresses interest in an insurance quote
    - *B*: Asks a set of questions to determine the appropiate quote, adapting to their respondes
    - *B*: Sends s request to use the quote genersation API tool along with necessary information collected from the user
    - *B*: Receives the response information from the API tool use, 
- *C*: Asks follow up questions
    - *B*: Answers follow up questions as needed
    - *B*: Guides the customer to the next steps in the insurance process and closes out the conversation

**Key**: In the real example that you write for your own use case, you might find it useful to write out the actual words in this interaction so that you can also get a sense of the ideal tone, response length, and level of detail you want Claude to have.


## Break the interaction into unique tasks

Before you start building, break down your ideal customer interaction into every task you want Claude to be able to perform. This ensures you can prompt and evaluate Claude for every task, and gives you a good sense of the range of interactions you need to account for when writing test cases.

1. Greeting and general guidance

- Warmly greet the customer and initiate conversation
- Provide general information about the company and interaction

2. Product Information

- Provide information about electric vehicle coverage
    - This will require that Claude have the necessary information in its context, and might imply that a RAG integration is necessary.
- Answer questions related to unique electric vehicle insurance needs
- Answer follow-up questions about the quote or insurance details
- Offer links to sources when appropriate

3. Conversation Management

- Stay on topic (car insurance)
- Redirect off-topic questions back to relevant subjects

4. Quote Generation

- Ask appropriate questions to determine quote eligibility
- Adapt questions based on customer responses
- Submit collected information to quote generation API
- Present the provided quote to the customer



## Establish success criteria

Criteria and benchmarks that can be used to evaluate how successfully Claude performs the defined tasks:
- Query comprehension accuracy
- Response relevance
- Response accuracy
- Citation provision relevance
- Topic adherence
- Content generation effectiveness
- Escalation efficiency

Evaluate the business impact of employing Claude for support:
- Sentiment maintenance
- Deflection rate
- Customer satisfaction score
- Average handle time


​



