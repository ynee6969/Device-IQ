import path from "node:path";
import { PrismaClient } from "@prisma/client";

declare global {
  // eslint-disable-next-line no-var
  var prisma: PrismaClient | undefined;
}

function resolveDatabaseUrl(rawUrl: string | undefined) {
  if (!rawUrl?.startsWith("file:")) {
    return rawUrl;
  }

  const sqliteTarget = rawUrl.slice("file:".length);
  const [filePath, query = ""] = sqliteTarget.split("?");

  if (!filePath) {
    return rawUrl;
  }

  const normalizedPath =
    path.isAbsolute(filePath) || /^[a-zA-Z]:[\\/]/.test(filePath)
      ? filePath
      : path.resolve(process.cwd(), filePath);

  const normalizedUrl = `file:${normalizedPath.replace(/\\/g, "/")}`;
  return query ? `${normalizedUrl}?${query}` : normalizedUrl;
}

const databaseUrl = resolveDatabaseUrl(process.env.DATABASE_URL);

if (databaseUrl) {
  process.env.DATABASE_URL = databaseUrl;
}

export const prisma =
  global.prisma ??
  new PrismaClient({
    datasources: databaseUrl
      ? {
          db: {
            url: databaseUrl
          }
        }
      : undefined,
    log: process.env.NODE_ENV === "development" ? ["warn", "error"] : ["error"]
  });

if (process.env.NODE_ENV !== "production") {
  global.prisma = prisma;
}
