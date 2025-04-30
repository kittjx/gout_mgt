// utils/formatters.js

/**
 * Formats a Date object or date string into a user-friendly string relative to today.
 * @param {Date|string|number} date - The date to format.
 * @returns {string} Formatted date string (e.g., "今天 HH:mm", "昨天 HH:mm", "MM-DD HH:mm", "YYYY-MM-DD HH:mm").
 */
export const formatDate = (date) => {
  let dateObj;
  if (date instanceof Date) {
    dateObj = date;
  } else {
    // Attempt to parse if it's not a Date object
    dateObj = new Date(date);
  }

  // Check if the conversion was successful
  if (isNaN(dateObj.getTime())) {
      console.warn("formatDate received an invalid date:", date);
      return '无效日期';
  }

  const year = dateObj.getFullYear();
  const month = String(dateObj.getMonth() + 1).padStart(2, '0');
  const day = String(dateObj.getDate()).padStart(2, '0');
  const hours = String(dateObj.getHours()).padStart(2, '0');
  const minutes = String(dateObj.getMinutes()).padStart(2, '0');

  const today = new Date();
  today.setHours(0, 0, 0, 0); // Set to start of today

  const yesterday = new Date(today);
  yesterday.setDate(today.getDate() - 1); // Set to start of yesterday

  const inputDay = new Date(dateObj);
  inputDay.setHours(0, 0, 0, 0); // Set to start of the input date's day

  if (inputDay.getTime() === today.getTime()) {
    return `今天 ${hours}:${minutes}`;
  } else if (inputDay.getTime() === yesterday.getTime()) {
    return `昨天 ${hours}:${minutes}`;
  } else {
    // Show month and day for current year, otherwise full date
    if (year === today.getFullYear()) {
      return `${month}-${day} ${hours}:${minutes}`;
    } else {
      return `${year}-${month}-${day} ${hours}:${minutes}`;
    }
  }
};

/**
 * Gets the current date and time formatted as 'YYYY-MM-DD HH:mm:ss'.
 * @returns {string} Formatted datetime string.
 */
export const getCurrentFormattedDateTimeString = () => {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
};