---
name: protos
description: Use when searching, finding, looking up, querying, browsing, discovering, or inspecting protocol buffer definitions, proto messages, services, enums, or fields via a proto search CLI.
---

# Protocol Buffer Documentation Search

**STOP** — Before proceeding, verify the proto search CLI is available by running `proto-cli --help`. If not found, stop and tell the user to install it.

A centralized repository of all protocol buffer services, messages, enums, and subfields is maintained in a shared API. The proto search CLI is used to interact with this API from the command line.

When you're asked to enumerate protocol buffers or find a model or search for models, you can use this skill to enhance or augment your capabilities. Some protobufs are not defined in the monorepo the user is currently working in. You might find `--json` output easier to work with as an agent.

## Usage

All commands accept the following options:

- `-l, --limit <n>`: Limit the number of results returned.
- `-j, --json`: Output results in JSON format.

### Search for protocol buffer messages

```bash
proto-cli search tax
```

### Get a specific message or proto definition

```bash
proto-cli get com.example.api.v4.Tax
```

### Search for a field or term within a specific message

```bash
proto-cli search --root com.example.api.v4.Tax name
```
