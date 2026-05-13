# AI Multi-Agent Country Intelligence System

## Objective
Build a multi-agent system that interacts with the REST Countries API to provide country intelligence, geographical analysis, and travel-related insights.

API Reference:
https://restcountries.com/

---

# Tasks

## 1. Analyze API Endpoints
Study the REST Countries API and understand the available endpoints and response structures.

---

## 2. Implement API Tool
Create a reusable API utility/tool that can:
- Send GET requests
- Handle query parameters
- Parse JSON responses
- Handle API failures and invalid country names
- Return structured responses

---

# Build Specialized Agents

## Root Agent (Master Coordinator)

### Responsibilities
- Understand user intent
- Route requests to appropriate specialized agents
- Combine responses from multiple agents
- Maintain conversation flow

### Example Queries
- "Tell me about India"
- "Compare India and Japan"
- "Which countries use Euro?"

---

# Specialized Agents

---

# 1. Country Info Agent

## Responsibilities
- Fetch country details
- Capital city
- Population
- Region
- Area
- Timezones
- Native names

## Example Queries
- "Tell me about India"
- "What is the capital of Germany?"

## Endpoints to Implement

### Get country by name
```bash
GET https://restcountries.com/v3.1/name/{country}
```

### Get country by country code
```bash
GET https://restcountries.com/v3.1/alpha/{code}
```

### Get all countries
```bash
GET https://restcountries.com/v3.1/all
```

---

# 2. Currency Agent

## Responsibilities
- Identify currencies
- Find countries using same currency
- Currency symbol and code extraction

## Example Queries
- "What currency is used in Japan?"
- "Which countries use Euro?"

## Endpoints to Implement

### Get all countries for currency analysis
```bash
GET https://restcountries.com/v3.1/all
```

### Get country by name
```bash
GET https://restcountries.com/v3.1/name/{country}
```

---

# 3. Language Agent

## Responsibilities
- Extract official languages
- Find multilingual countries
- Find countries sharing same language

## Example Queries
- "Which countries speak French?"
- "Official languages of Switzerland"

## Endpoints to Implement

### Get country by language
```bash
GET https://restcountries.com/v3.1/lang/{language}
```

### Get country by name
```bash
GET https://restcountries.com/v3.1/name/{country}
```

### Get all countries
```bash
GET https://restcountries.com/v3.1/all
```

---

# 4. Geography Agent

## Responsibilities
- Border countries
- Continents
- Regions and subregions
- Geographic analysis

## Example Queries
- "Which countries border India?"
- "Countries in South America"

## Endpoints to Implement

### Get countries by region
```bash
GET https://restcountries.com/v3.1/region/{region}
```

### Get country by name
```bash
GET https://restcountries.com/v3.1/name/{country}
```

### Get country by country code
```bash
GET https://restcountries.com/v3.1/alpha/{code}
```

---

# 5. Population Analytics Agent

## Responsibilities
- Population comparisons
- Population rankings
- Density analysis

## Example Queries
- "Top 10 populated countries"
- "Compare India and China population"

## Endpoints to Implement

### Get all countries
```bash
GET https://restcountries.com/v3.1/all
```

### Get countries by region
```bash
GET https://restcountries.com/v3.1/region/{region}
```

### Get country by name
```bash
GET https://restcountries.com/v3.1/name/{country}
```

---

# 6. Comparison Agent

## Responsibilities
Compare:
- Population
- Area
- Currency
- Languages
- Capital
- Region

## Example Queries
- "Compare India and USA"
- "Japan vs South Korea"

## Endpoints to Implement

### Get country by name
```bash
GET https://restcountries.com/v3.1/name/{country}
```

### Get country by code
```bash
GET https://restcountries.com/v3.1/alpha/{code}
```

---

# 7. Flag & Symbols Agent (Optional)

## Responsibilities
- Country flags
- Coat of arms
- National symbols

## Example Queries
- "Show Japan flag"

## Endpoints to Implement

### Get country by name
```bash
GET https://restcountries.com/v3.1/name/{country}
```

### Get all countries
```bash
GET https://restcountries.com/v3.1/all
```

---

# Requirements

## Framework
Use:
```bash
google-adk
```

---

# API Handling Requirements

The system should:
- Handle invalid country names gracefully
- Handle empty API responses
- Parse nested JSON responses
- Return structured outputs
- Implement proper exception handling

---

# Multi-Agent Coordination

The root agent must:
- Delegate tasks intelligently
- Identify the correct specialized agent
- Aggregate outputs from multiple agents

---

# Suggested Architecture

```text
                    ┌─────────────────┐
                    │   Root Agent    │
                    └────────┬────────┘
                             │
       ┌──────────────────────────────────────┐
       │                                      │
┌───────────────┐                    ┌────────────────┐
│ Country Agent │                    │ Comparison Ag.│
└───────────────┘                    └────────────────┘
       │                                      │
 ┌────────────┬─────────────┬─────────────┬─────────────┐
 │            │             │             │             │
▼            ▼             ▼             ▼             ▼
Currency   Language    Geography    Population    Regional
 Agent      Agent        Agent        Agent         Agent
```

---

# Example Queries

## Basic Queries
- "Tell me about India"
- "Capital of Brazil"
- "Currency used in Japan"

---

## Intermediate Queries
- "Countries speaking Spanish"
- "Countries bordering China"

---