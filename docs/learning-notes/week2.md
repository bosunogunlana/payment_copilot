## Tool Call Execution Flow

```text
Question + tool definitions
         ↓
    Model request
        ↓
Application checks limits
        ↓
Validate → authorize → execute
        ↓
  Evidence or typed error
        ↓
Return correlated tool result
        ↓
  Model requests more work?
      ↙             ↘
    Yes             No
  repeat        final answer
```

## Journey of a Question to Answer via ToolLoop
- ToolLoop provides interface for model call and tool execution as needed
- ToolModel provides interface for LLM clients but build the request object and parse response in a way that the application understands

The execution flow from question i.e. What is the status of payment pay-shared?, to LLM response goes through this:
- ToolModel is initialized with the the LLM client and limits (token and timeout) that the client must respect
  - ToolModel is only able to make a single request and response cycle
- ToolGateway defined the interface for the ToolLoop/Model to execute tools on behalf of the LLM
- ToolLoop is initialized with both the ToolModel and ToolGateway: The run sequence
  - The model makes a request and return a response (the model limits like output token limit and timeout is enforced at this level)
    - the number of models calls that can be made is guided by the max_model_turn 
  - the response from the model is transformed to what the application understands at the ToolModel level
  - If the response requires a tool_call, the ToolLoop instance will check if the application can still permit such call via the max tool steps check
    - If the turn is allowed and not final text output the model turn will be passed to ToolGateway which will validate, authorize and execute the tool
    - The loop then appends the tool result to the conversation using the original call_id and proceeds to send the conversation to the model again which can either request for more evidence ot a final answer
  - If it's final text turn, no gateway execution will happen, the final answer will be returned through the LoopResult

- The LLM Provider authentication happens at the provider level and invalid credentials is rejected
- ToolGateway invokes its injected authorization function using TrustedContext, the tool name, and validated payment ID. TrustedContext carries organization and request identity.
- ToolModel never authorizes payment data access and the model supplied arguments cann't override TrustedContext
- RetryExecutor supports bounded retries, but the current ToolLoop calls the gateway directly. 
  - Recovery is exercised separately by the evidence runner. It retries classified transient failures—including timeout and synthetic 500 errors—not every timeout indiscriminately.

Check scripts/week2.py for live walkthrough loop of the flow.