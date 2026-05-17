import { spawnSync } from "node:child_process";
import { existsSync, readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const projectRoot = path.resolve(scriptDir, "..");

function readDatabaseUrlFromEnvFiles(projectRoot) {
  const envCandidates = [
    ".env.development.local",
    ".env.local",
    ".env.development",
    ".env"
  ];

  for (const fileName of envCandidates) {
    const filePath = path.join(projectRoot, fileName);
    if (!existsSync(filePath)) {
      continue;
    }

    const lines = readFileSync(filePath, "utf8").split(/\r?\n/);
    for (const line of lines) {
      const trimmed = line.trim();
      if (!trimmed || trimmed.startsWith("#")) {
        continue;
      }

      const separatorIndex = trimmed.indexOf("=");
      if (separatorIndex === -1) {
        continue;
      }

      const key = trimmed.slice(0, separatorIndex).trim();
      if (key !== "DATABASE_URL") {
        continue;
      }

      const rawValue = trimmed.slice(separatorIndex + 1).trim();
      return rawValue.replace(/^['"]|['"]$/g, "");
    }
  }

  return "";
}

function resolveSchemaPath() {
  const url =
    process.env.DATABASE_URL?.trim() ??
    readDatabaseUrlFromEnvFiles(projectRoot);

  if (url.startsWith("file:")) {
    return "prisma/schema.sqlite.prisma";
  }

  return "prisma/schema.prisma";
}

const schemaPath = resolveSchemaPath();
const prismaCliEntry = path.join(projectRoot, "node_modules", "prisma", "build", "index.js");
const prismaArgs = ["generate", "--schema", schemaPath];
const generatedClientPath = path.join(projectRoot, "node_modules", ".prisma", "client", "index.d.ts");

const result = spawnSync(process.execPath, [prismaCliEntry, ...prismaArgs], {
  stdio: "pipe",
  cwd: projectRoot,
  env: process.env
});

const stdout = result.stdout?.toString() ?? "";
const stderr = result.stderr?.toString() ?? "";

if (stdout) {
  process.stdout.write(stdout);
}

if (stderr) {
  process.stderr.write(stderr);
}

if (result.status !== 0) {
  const combinedOutput = `${stdout}\n${stderr}`;

  if (combinedOutput.includes("EPERM: operation not permitted, unlink") && existsSync(generatedClientPath)) {
    process.stderr.write(
      "\n[generate-prisma-client] Prisma client already exists and the local files are locked. Continuing.\n"
    );
    process.exit(0);
  }

  if (result.error) {
    process.stderr.write(`\n[generate-prisma-client] ${result.error.message}\n`);
  }

  process.exit(result.status ?? 1);
}
