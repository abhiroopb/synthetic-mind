---
name: trakt
description: Track TV shows and movies with Trakt.tv. Search, get watchlist, history, up-next, recommendations, trending, calendar, ratings, stats, add/remove from watchlist, mark watched, rate, and check in. Use when asked about what to watch, TV shows, movies, watch history, or Trakt.
---

# Trakt Skill

Interact with Trakt.tv for TV show and movie tracking via a local REST API running on port 7273 (part of AmpClaw).

## Important

**Trakt is already authenticated.** Do NOT ask the user for credentials, API keys, or tokens. All requests go through the local API which handles auth automatically.

## API Base URL

```
http://localhost:7273
```

## Endpoints

### Read Operations (GET)

| Endpoint | Params | Description |
|---|---|---|
| `/trakt/stats` | — | User stats (total watched, minutes, etc.) |
| `/trakt/watchlist` | `?type=movies\|shows` | Get watchlist items |
| `/trakt/history` | `?type=movies\|shows&limit=20` | Recently watched |
| `/trakt/watched` | `?type=shows\|movies` | All watched shows/movies with progress |
| `/trakt/up-next` | — | Next episodes to watch for in-progress shows |
| `/trakt/calendar` | `?type=shows\|movies&days=7` | Upcoming episodes/movies |
| `/trakt/recommendations` | `?type=shows\|movies&limit=10` | Personalized recommendations |
| `/trakt/trending` | `?type=shows\|movies&limit=10` | Currently trending |
| `/trakt/popular` | `?type=shows\|movies&limit=10` | Most popular |
| `/trakt/search` | `?q=query&type=movie\|show` | Search for shows/movies |
| `/trakt/ratings` | `?type=movies\|shows` | User's rated items |
| `/trakt/collection` | `?type=shows\|movies` | User's collection |
| `/trakt/status` | — | API health check |

### Write Operations (POST)

#### Add to Watchlist
```
POST /trakt/watchlist
{"movies": [{"ids": {"trakt": 123}}], "shows": [{"ids": {"trakt": 456}}]}
```

#### Remove from Watchlist
```
POST /trakt/watchlist/remove
{"movies": [{"ids": {"trakt": 123}}]}
```

#### Mark as Watched
```
POST /trakt/history
{"movies": [{"ids": {"trakt": 123}}], "shows": [{"ids": {"trakt": 456}}]}
```

#### Rate an Item
```
POST /trakt/ratings
{"movies": [{"ids": {"trakt": 123}, "rating": 10}]}
```

#### Check In (currently watching)
```
POST /trakt/checkin
{"movie": {"ids": {"trakt": 123}}}
```

## Usage with curl (via Bash tool)

Always use `curl` via the Bash tool to call these endpoints. Examples:

```bash
# Get stats
curl -s http://localhost:7273/trakt/stats

# Search for a movie
curl -s "http://localhost:7273/trakt/search?q=Hail+Mary&type=movie"

# Mark a movie as watched and rate it
curl -s -X POST http://localhost:7273/trakt/history -H "Content-Type: application/json" -d "{\"movies\":[{\"ids\":{\"trakt\":12345}}]}"
curl -s -X POST http://localhost:7273/trakt/ratings -H "Content-Type: application/json" -d "{\"movies\":[{\"ids\":{\"trakt\":12345},\"rating\":10}]}"

# Get what to watch next
curl -s http://localhost:7273/trakt/up-next

# Get watchlist
curl -s http://localhost:7273/trakt/watchlist
```

## Workflow

1. **To find an item:** Use `/trakt/search?q=...` to get the Trakt ID
2. **To add/rate/mark watched:** Use the Trakt ID from search in POST requests
3. **To browse:** Use watchlist, up-next, trending, recommendations, or calendar
4. **Always use the `trakt` ID** from the `ids` object in search results (not imdb/tmdb)
