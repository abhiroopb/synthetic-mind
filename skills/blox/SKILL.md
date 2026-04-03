---
name: blox
description: "Delegate work to cloud workstations. Use when the user wants to offload, dispatch, launch, provision, manage, or develop on a remote cloud workstation, or run commands and execute prompts on a cloud workstation."
metadata:
  version: "0.1.0"
  status: beta
---

# Cloud Workstations

Manage remote development workstations using a CLI tool. Workstations are cloud environments backed by git repos where you can run agent prompts, execute commands, and develop remotely.

**STOP** if the cloud workstation CLI is not installed or available. See `SETUP.md` for installation.

## Core Workflows

### Prompt-Based Changes

```bash
ws start my-feature org/my-service

ws prompt my-feature "Add input validation to the CreateUser endpoint"

ws diff my-feature

ws delete my-feature
```

### Manual Command Execution

```bash
ws exec my-feature make test

ws commands my-feature

ws output my-feature <process-id>

ws get-file my-feature src/main.go
```

## Starting a Workstation

```bash
ws start <name> <git-repo>
```

`<name>` is a human-readable identifier, `<git-repo>` is the repository to clone (e.g. `org/my-service`).

To start from a specific branch, append `?ref=<branch>`:

```bash
ws start my-ws "github.com/org/my-repo?ref=feature-branch"
```

Run the presetup command first if you've never created a workstation before (creates your namespace).

## Running Prompts

Execute an agent prompt on a workstation:

```bash
ws prompt <name> "<prompt>"
```

## Executing Commands

```bash
ws exec <name> <command> [args...]
```

Use `ws run` instead for quick commands that don't need to be persisted.

## Monitoring Processes

```bash
ws commands <name>
ws output <name> <process-id>
```

Aliases: `ws cmds`, `ws ps`

## Retrieving Files

```bash
ws get-file <name> <path>
ws get-file <name> config.yaml -o local-config.yaml
```

## Workstation Lifecycle

```bash
ws list          # list workstations (alias: ls)
ws info <name>   # detailed status
ws resume <name> # resume suspended workstation
ws delete <name> # permanently remove
ws ssh <name>    # SSH (not supported on k8s, use web terminal)
ws diff <name>   # git diff since checkout
```

## Agent Control Protocol (ACP)

Start a bidirectional JSON-RPC session with an agent on the workstation:

```bash
acp <name>
```

See `references/commands.md` for the full command reference and troubleshooting.
