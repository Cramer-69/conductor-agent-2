# Skills (Superpowers)

Skills are reusable prompt templates that customize how the Conductor Agent responds. Activating a skill prepends a specialized system prompt to every query for the remainder of the session, letting you switch the agent's behavior on the fly.

## Listing Available Skills

```
/skills
```

Prints each loaded skill with its name and a short description, for example:

```
Available Superpowers:
• brainstorming: Generate creative ideas and explore multiple angles of a problem...
• tdd: Write test-driven development workflows with red-green-refactor cycles...
```

## Activating a Skill

```
/skill <name>
```

Replaces the current skill prompt with the one named `<name>`. Every query you send after activation will use that skill's prompt until you activate a different skill or restart the session.

**Example**

```
/skill brainstorming
```

Output:

```
Activated Superpower: brainstorming
```

If the skill name is not found, the agent prints an error and suggests running `/skills` to see the available options.

## How Skills Work

When a skill is active the agent builds its system prompt as:

```
<skill prompt>

---

<base system prompt>
```

The base system prompt gives the agent access to your conversation history across platforms. The skill prompt sits above it and shapes the agent's tone, format, and reasoning style for that task.

Skills do **not** persist across sessions. You must re-activate a skill each time you start the CLI.

## Creating a Custom Skill

Skills are discovered automatically from subdirectories inside the `skills/` folder. To add a skill:

1. Create a new directory under `skills/` whose name is the skill identifier you will use with `/skill`:

   ```
   skills/
   └── my-skill/
       └── SKILL.md
   ```

2. Write a `SKILL.md` file inside that directory. The **first line** becomes the skill's description shown by `/skills`. The full file content (up to 500 characters) is used as the system prompt injected into every query.

   ```markdown
   # My Custom Skill
   
   You are an expert at … Respond in a concise, bullet-point style …
   ```

3. Restart the CLI. The new skill will be listed by `/skills` and can be activated with `/skill my-skill`.

### Example `SKILL.md` — TDD

```markdown
# Test-Driven Development Coach

Follow a strict red-green-refactor cycle. For every feature request:
1. Write a failing test first.
2. Write the minimal code to make it pass.
3. Refactor while keeping tests green.
Always show the test before the implementation.
```

## Related Commands

| Command | Description |
|---------|-------------|
| `/skills` | List all available skills |
| `/skill <name>` | Activate the named skill |
| `/help` | Show all CLI commands |
