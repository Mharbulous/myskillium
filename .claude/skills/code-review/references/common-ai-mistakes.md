# Common AI-Generated Code Mistakes

Patterns to watch for when reviewing code produced by AI assistants.

---

## 1. Hallucinated APIs

**What it is:** AI invents methods, functions, or libraries that don't exist.

**Examples:**
```python
# AI invented this method - it doesn't exist
result = requests.fetch_async(url)  # Should be: requests.get(url)

# Made-up pandas method
df.auto_clean_nulls()  # No such method

# Invented library
from fast_json import parse  # Library doesn't exist
```

**Detection:**
- Verify imports against actual package APIs
- Test unfamiliar method calls
- Check library documentation

---

## 2. Outdated Patterns

**What it is:** AI uses deprecated APIs or old coding styles from training data.

**Examples:**
```python
# Python 2 style (deprecated)
print "Hello"  # Should be: print("Hello")

# Old async pattern
@asyncio.coroutine  # Should be: async def

# Deprecated method
os.popen(cmd)  # Should use: subprocess.run()
```

**Detection:**
- Check deprecation warnings
- Compare against current documentation
- Look for patterns from old Stack Overflow answers

---

## 3. Ignored Constraints

**What it is:** AI writes code that works generally but ignores project-specific rules.

**Examples:**
```python
# Project uses snake_case, AI uses camelCase
def getUserData():  # Should be: get_user_data()

# Project has no external dependencies rule
import pandas  # Project uses standard library only

# Project uses pathlib, AI uses os.path
import os
os.path.join()  # Should use: pathlib.Path
```

**Detection:**
- Compare against project conventions
- Check CLAUDE.md/style guides
- Look for pattern breaks from existing code

---

## 4. Missing Edge Cases

**What it is:** AI handles happy path but misses boundary conditions.

**Examples:**
```python
# No empty list check
def get_first(items):
    return items[0]  # IndexError if empty

# No null check
def process(data):
    return data.strip()  # AttributeError if None

# No bounds check
def get_item(arr, idx):
    return arr[idx]  # No validation of idx
```

**Detection:**
- Test with empty inputs
- Test with None/null
- Test boundary values (0, -1, max)

---

## 5. Security Blind Spots

**What it is:** AI optimizes for functionality, not security.

**Examples:**
```python
# SQL injection vulnerability
query = f"SELECT * FROM users WHERE id = {user_id}"

# Command injection
os.system(f"echo {user_input}")

# Path traversal
open(f"uploads/{filename}")  # No sanitization

# Exposed credentials
api_key = "sk-1234567890"  # Hardcoded secret
```

**Detection:**
- Look for string interpolation in queries/commands
- Check all user input paths
- Scan for literal secrets

---

## 6. Over-Abstraction

**What it is:** AI creates unnecessary complexity for simple problems.

**Examples:**
```python
# Simple task, unnecessary abstraction
class DataProcessorFactory:
    def create_processor(self, type):
        return {"csv": CSVProcessor, "json": JSONProcessor}[type]()

# Could just be:
def process_csv(data): ...
def process_json(data): ...

# Unnecessary design pattern
class SingletonMeta(type):
    _instances = {}
    # ... 20 more lines for a simple config object
```

**Detection:**
- Ask "could this be simpler?"
- Count abstraction layers
- Check if patterns are justified by requirements

---

## 7. Incorrect Error Handling

**What it is:** AI either swallows errors silently or handles them incorrectly.

**Examples:**
```python
# Silent failure
try:
    process_data()
except:
    pass  # What went wrong?

# Too broad exception
try:
    result = api_call()
except Exception:
    return None  # Hides specific issues

# Wrong exception type
try:
    data = json.loads(text)
except ValueError:  # Should be: json.JSONDecodeError
    pass
```

**Detection:**
- Look for bare except clauses
- Check exception types match possible errors
- Verify errors are logged or propagated appropriately

---

## 8. Test Deletion/Skipping

**What it is:** AI deletes or skips tests instead of fixing the code.

**Examples:**
```python
# Test mysteriously removed from suite
# (compare with git diff)

# Test skipped without reason
@pytest.mark.skip  # Why?
def test_authentication(): ...

# Test always passes
def test_feature():
    assert True  # Placeholder that never fails
```

**Detection:**
- Compare test count before/after changes
- Look for new skip decorators
- Check test assertions are meaningful

---

## 9. Repetitive Code

**What it is:** AI generates similar code blocks instead of factoring out common logic.

**Examples:**
```python
# Same pattern repeated
def get_user(id):
    conn = get_connection()
    result = conn.execute(f"SELECT * FROM users WHERE id = {id}")
    conn.close()
    return result

def get_order(id):
    conn = get_connection()
    result = conn.execute(f"SELECT * FROM orders WHERE id = {id}")
    conn.close()
    return result

# Should use context manager or helper
```

**Detection:**
- Look for similar code blocks
- Check for copy-paste patterns
- Identify common logic to extract

---

## 10. Incorrect Async/Concurrency

**What it is:** AI mishandles async patterns or introduces race conditions.

**Examples:**
```python
# Missing await
async def fetch_data():
    data = api.get_data()  # Should be: await api.get_data()
    return data

# Race condition
class Counter:
    value = 0
    def increment(self):
        self.value += 1  # Not thread-safe

# Blocking call in async context
async def process():
    time.sleep(1)  # Should be: await asyncio.sleep(1)
```

**Detection:**
- Check all async calls have await
- Look for shared mutable state
- Verify blocking calls aren't in async context

---

## Statistics

Research shows:
- **45%** of AI-generated code contains security vulnerabilities
- AI code creates **1.7x more issues** in PR analysis
- AI PRs average **10.83 issues** vs **6.45 for human code**
- **89%** work functionally, but security/performance issues hidden

---

## Review Mindset

1. **Treat as draft** - AI code is a starting point, not final
2. **Verify, don't trust** - Test unfamiliar APIs/methods
3. **Check context** - Does it match project patterns?
4. **Test adversarially** - What inputs break it?
5. **Question "working"** - Functional != secure/performant
