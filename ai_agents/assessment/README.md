# Assessment: AI Agents with Fake Store API

## Objective
Build a multi-agent system that interacts with the [Fake Store API](https://fakestoreapi.com/docs) to manage an e-commerce platform's data.

## Tasks
1. **Analyze API Endpoints**: Refer to the [Fake Store API Documentation](https://fakestoreapi.com/docs).
2. **Implement API Tool**: Create a robust tool that can handle GET, POST, PATCH, and DELETE requests for various resources (Products, Carts, Users).
3. **Build Specialized Agents**:
    - **Products Agent**: Handle GET, POST, PATCH, and DELETE operations for products.
    - **Carts Agent**: Handle GET, POST, PATCH, and DELETE operations for shopping carts.
    - **Users Agent**: Handle GET, POST, PATCH, and DELETE operations for user profiles.
4. **Coordinate with a Root Agent**: Implement a master agent that can delegate tasks to the specialized agents based on user queries.

## Requirements
- Use the `google-adk` framework.
- All major HTTP methods (GET, POST, PATCH, DELETE) must be represented as agent capabilities.
- Ensure proper handling of JSON data and HTTP error statuses.

## Evaluation Criteria
- **Functional Correctness**: Agents should correctly perform the requested API operations.
- **Agent Intelligence**: The root agent should accurately route requests to the correct specialized agent.
- **Code Quality**: Clean implementation of tools and agent configurations.
