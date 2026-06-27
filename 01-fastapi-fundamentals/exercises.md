# Exercises — Session 01: FastAPI Fundamentals

Each part mixes everyday Kenyan-context questions with AI-engineering-flavoured ones, since both kinds of endpoints keep showing up through this course.

## Part A — Path Parameters

1. Build a GET endpoint `/matatu/{route_number}` that returns the route number and a fixed fare, e.g. `{"route": "32", "fare_ksh": 100}`.
2. Build a GET endpoint `/county/{name}` that returns `{"county": name, "capital": "unknown"}` for any county name typed in.
3. Build a GET endpoint `/bot/{bot_name}` that returns `{"bot": bot_name, "status": "online"}` — imagine this is how a user checks which AI assistant they're talking to.

## Part B — Query Parameters

1. Build a GET endpoint `/weather` that takes `town` (default `"Nairobi"`) and `unit` (default `"celsius"`) as query parameters and returns both.
2. Build a GET endpoint `/menu` that takes a `category` query parameter (default `"all"`) for a small food kiosk, returning `{"category": category}`.
3. Build a GET endpoint `/faq` that takes `topic` and `max_results` (default `3`) query parameters, for filtering helpdesk questions by topic.

## Part C — Request Body with Pydantic

1. Build a Pydantic model `Order` with `customer_name` and `item`, and a POST endpoint `/order` for a small Mama Mboga shop that echoes back what was ordered.
2. Build a Pydantic model `Ticket` with `sender` and `message`, and a POST endpoint `/support` that echoes back the sender and message — this is the basic shape of any AI support-bot intake endpoint.
3. Build a Pydantic model `Booking` with `passenger_name` and `route`, and a POST endpoint `/book` for a matatu booking app that echoes the booking details back.

## Part D — Response Models and Error Handling

1. Add a response model `BookInfo` (`title`, `author`, `available: bool`) to a GET `/book/{title}` endpoint for a small library, raising a 404 if the title is not in your list.
2. Add a response model `BotReply` (`question`, `answer`, `confidence`) to a POST `/ask-bot` endpoint, raising a 404 with detail `"Topic not supported"` if the topic sent is not in a small allowed list.
3. Add a response model `PriceCheck` (`item`, `price_ksh`) to a GET `/price/{item}` endpoint for a shop, raising a 404 if the item is not stocked.

## Part E — Challenge: Combine Everything

1. Build a small "AI Support Intake API" with:
   - a GET `/` health-check endpoint
   - a GET `/agent/{agent_name}` path endpoint with a 404 for unknown agents
   - a GET `/tickets` query endpoint that filters by `status` (default `"open"`) and `limit` (default `5`)
   - a POST `/ticket` endpoint using a Pydantic request model (`customer_name`, `issue`) and a Pydantic response model (`ticket_id`, `customer_name`, `issue`, `priority`) that always returns `priority` as `"normal"`
2. Test every endpoint of your Challenge API using the automatic docs at `/docs` before moving on — don't just read the code, run it.
