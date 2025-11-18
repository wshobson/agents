# Twitter Timeline Case Study

## Challenge
- 400M+ users
- 6K tweets/sec average
- 70K tweets/sec peak
- Real-time timeline delivery

## Architecture Evolution

### Approach 1: Pull on Read (Fan-out on Read)
```
User requests timeline
  ↓
Query: SELECT * FROM tweets 
       WHERE user_id IN (following_list)
       ORDER BY timestamp DESC
  ↓
Merge and sort
```

**Problems**:
- Slow for users with many followers
- Heavy database load
- Poor user experience

### Approach 2: Push on Write (Fan-out on Write)
```
User posts tweet
  ↓
Fan out to all followers' timelines
  ↓
Pre-computed timelines in cache
```

**Problems**:
- Celebrity problem (millions of followers)
- Write amplification
- Stale follower lists

### Approach 3: Hybrid
```
Normal users: Fan-out on write
Celebrities: Fan-out on read
Merge at read time
```

**Implementation**:
```python
def get_timeline(user_id):
    # Get pre-computed timeline (normal follows)
    timeline = cache.get(f"timeline:{user_id}")

    # Merge with celebrity tweets (computed on-demand)
    celebrity_follows = get_celebrity_follows(user_id)
    celebrity_tweets = get_recent_tweets(celebrity_follows)

    return merge_timelines(timeline, celebrity_tweets)
```

## Caching Strategy

### L1: In-Process Cache
- JVM heap cache
- Sub-millisecond access
- Limited size

### L2: Redis
- Distributed cache
- 1-5ms latency
- Timeline data, user profiles

### L3: Database
- Long-term storage
- 10-50ms latency
- MySQL (sharded)

## Lessons
- One size doesn't fit all
- Hybrid approaches for heterogeneous data
- Multi-tier caching critical
- Pre-computation trades write for read performance
