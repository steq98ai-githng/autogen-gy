// security-utils.ts
// Central location for security-related utility functions

/**
 * Sanitizes avatar/image URLs to prevent untrusted external URL injection.
 * Allows only http(s) URLs that resolve to the current origin.
 */
export const sanitizeUrl = (url: string | undefined | null): string => {
  if (!url || typeof url !== "string") return "";

  try {
    const parsedUrl = new URL(url, window.location.origin);

    if (parsedUrl.protocol !== "http:" && parsedUrl.protocol !== "https:") {
      return "";
    }

    if (parsedUrl.origin !== window.location.origin) {
      return "";
    }

    return parsedUrl.toString();
  } catch {
    return "";
  }
};

/**
 * Sanitizes redirect URLs to prevent open redirect vulnerabilities
 * Only allows relative URLs or URLs to the current origin
 */
export const sanitizeRedirectUrl = (url: string | undefined | null): string => {
  if (!url || typeof url !== "string") return "/";

  // Allow relative URLs
  if (url.startsWith("/")) return url;

  try {
    // For absolute URLs, check if they point to your domain
    const urlObj = new URL(url);
    if (urlObj.origin === window.location.origin) {
      return url;
    }
  } catch (e) {
    // Invalid URL
  }

  // Default to homepage for security
  return "/";
};

/**
 * Validates if a message event is from a trusted origin
 */
export const isValidMessageOrigin = (origin: string): boolean => {
  const trustedOrigins = [
    window.location.origin,
    "http://localhost:8000",
    "http://localhost:8081",
  ];

  return trustedOrigins.includes(origin);
};

/**
 * Validates user object structure to prevent prototype pollution
 */
export const isValidUserObject = (user: any): boolean => {
  return (
    user &&
    typeof user === "object" &&
    typeof user.id === "string" &&
    typeof user.name === "string" &&
    (user.email === undefined || typeof user.email === "string") &&
    (user.avatar_url === undefined || typeof user.avatar_url === "string") &&
    (user.provider === undefined || typeof user.provider === "string")
  );
};
