/**
 * Compatibility helper functions for older browsers
 */

// Safe object property access (alternative to optional chaining)
export function safeGet(obj, path, defaultValue) {
  if (!obj) return defaultValue;
  
  const keys = path.split('.');
  let current = obj;
  
  for (let i = 0; i < keys.length; i++) {
    if (current === null || current === undefined) {
      return defaultValue;
    }
    current = current[keys[i]];
  }
  
  return current !== undefined ? current : defaultValue;
}

// Safe nullish coalescing alternative
export function safeDefault(value, defaultValue) {
  return (value === null || value === undefined) ? defaultValue : value;
}

// Safe JSON parse
export function safeJsonParse(str, defaultValue) {
  try {
    return JSON.parse(str);
  } catch (e) {
    console.error('Error parsing JSON:', e);
    return defaultValue;
  }
}

// Safe date parsing
export function safeParseDate(dateStr) {
  try {
    const date = new Date(dateStr);
    return isNaN(date.getTime()) ? new Date() : date;
  } catch (e) {
    console.error('Error parsing date:', e);
    return new Date();
  }
}

// Safe array operations
export function safeArrayOperation(array, operation, ...args) {
  if (!Array.isArray(array)) {
    console.error('Not an array:', array);
    return [];
  }
  
  try {
    return array[operation](...args);
  } catch (e) {
    console.error(`Error in array.${operation}:`, e);
    return [];
  }
}

// Safe function call
export function safeCall(fn, ...args) {
  if (typeof fn !== 'function') {
    return undefined;
  }
  
  try {
    return fn(...args);
  } catch (e) {
    console.error('Error calling function:', e);
    return undefined;
  }
}

// Check if browser supports modern features
export function supportsModernJS() {
  return window.SUPPORTS_MODERN_JS === true;
}