import time
from abc import ABC, abstractmethod


# Define the interface for the Real Subject
class DatabaseQuery(ABC):
    @abstractmethod
    def execute_query(self, query):
        pass


# Real Subject: Represents the actual database
class RealDatabaseQuery(DatabaseQuery):
    def execute_query(self, query):
        print(f"Executing query: {query}")
        # Simulate a database query and return the results
        return f"Results for query: {query}"


# Proxy: Caching Proxy for Database Queries
class CacheProxy(DatabaseQuery):
    def __init__(self, real_database_query, cache_duration_seconds):
        self._real_database_query = real_database_query
        self._cache = {}
        self._cache_duration = cache_duration_seconds

    def execute_query(self, query):
        if query in self._cache and time.time() - self._cache[query]["timestamp"] <= self._cache_duration:
            # Return cached result if it's still valid
            print(f"CacheProxy: Returning cached result for query: {query}")
            return self._cache[query]["result"]
        else:
            # Execute the query and cache the result
            result = self._real_database_query.execute_query(query)
            self._cache[query] = {"result": result, "timestamp": time.time()}
            return result
