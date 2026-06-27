#!/usr/bin/env node
const fs = require("fs");
const os = require("os");
const path = require("path");

function help() {
  console.log(`Usage: openai-imagegen-skill [--dest <path>] [--force]

Install skills/openai-imagegen into $CODEX_HOME/skills or ~/.codex/skills.`);
}

function parseArgs(argv) {
  let dest = null;
  let force = false;

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--dest") {
      dest = argv[++i];
      if (!dest) {
        throw new Error("--dest requires a path");
      }
    } else if (arg === "--force") {
      force = true;
    } else if (arg === "-h" || arg === "--help") {
      help();
      process.exit(0);
    } else {
      throw new Error(`Unknown argument: ${arg}`);
    }
  }

  return { dest, force };
}

function copyRecursive(source, target, force) {
  if (!fs.existsSync(source)) {
    throw new Error(`Skill source not found: ${source}`);
  }

  if (fs.existsSync(target)) {
    if (!force) {
      throw new Error(`Destination already exists: ${target}. Re-run with --force to replace it.`);
    }
    fs.rmSync(target, { recursive: true, force: true });
  }

  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.cpSync(source, target, { recursive: true });
}

function main() {
  const { dest, force } = parseArgs(process.argv.slice(2));
  const source = path.resolve(__dirname, "..", "skills", "openai-imagegen");
  const codexHome = process.env.CODEX_HOME || path.join(os.homedir(), ".codex");
  const target = path.resolve(dest || path.join(codexHome, "skills", "openai-imagegen"));

  copyRecursive(source, target, force);
  console.log(target);
}

try {
  main();
} catch (error) {
  console.error(error.message);
  process.exit(1);
}
