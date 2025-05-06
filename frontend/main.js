// Add polyfill for older browsers
(function() {
  // Check if the browser supports modern features
  var supportsModernJS = false;
  try {
    // Test for optional chaining
    eval('var test = {a:{b:1}}; var x = test?.a?.b;');
    // Test for nullish coalescing
    eval('var y = null ?? "default";');
    supportsModernJS = true;
  } catch (e) {
    console.warn('Browser does not support modern JavaScript features. Using compatibility mode.');
    supportsModernJS = false;
  }
  
  // Set a flag for the app to use
  window.SUPPORTS_MODERN_JS = supportsModernJS;
})();

// Add this at the top of the file
window.addEventListener('error', function(event) {
  console.error('Global error event:', event.error);
  console.error('Error message:', event.message);
  console.error('Error source:', event.filename, 'line:', event.lineno, 'col:', event.colno);
  
  // Log additional details for syntax errors
  if (event.error instanceof SyntaxError) {
    console.error('SyntaxError detected. This might be due to unsupported JavaScript features in this browser.');
    console.error('Browser info:', navigator.userAgent);
  }
  
  // Prevent the error from being reported to the console again
  event.preventDefault();
  
  // Show error to user
  uni.showToast({
    title: 'An error occurred. Please try again.',
    icon: 'none',
    duration: 3000
  });
  
  return true;
});

// Add this for unhandled promise rejections
window.addEventListener('unhandledrejection', function(event) {
  console.error('Unhandled promise rejection:', event.reason);
  console.error('Browser info:', navigator.userAgent);
  
  // Prevent the error from being reported to the console again
  event.preventDefault();
  
  // Show error to user
  uni.showToast({
    title: 'An error occurred. Please try again.',
    icon: 'none',
    duration: 3000
  });
  
  return true;
});

import App from './App'

// #ifndef VUE3
import Vue from 'vue'
import './uni.promisify.adaptor'
Vue.config.productionTip = false
App.mpType = 'app'

// Add a global mixin to handle component errors
Vue.mixin({
  errorCaptured: function(err, vm, info) {
    console.error('Component error captured:', err);
    console.error('Component:', vm.$options.name || 'anonymous');
    console.error('Error info:', info);
    
    // Show error to user
    uni.showToast({
      title: 'Component error occurred',
      icon: 'none',
      duration: 3000
    });
    
    // Return false to prevent error propagation
    return false;
  }
});

const app = new Vue({
  ...App
})
app.$mount()

// Add global error handler with more detailed logging
app.config.errorHandler = function(err, vm, info) {
  console.error('Global error:', err);
  console.error('Error info:', info);
  console.error('Error stack:', err && err.stack ? err.stack : 'No stack trace available');
  console.error('Browser info:', navigator.userAgent);
  
  // Check if it's a syntax error
  if (err instanceof SyntaxError) {
    console.error('SyntaxError detected. This might be due to unsupported JavaScript features in this browser.');
  }
  
  // Show error to user in development
  if (process.env.NODE_ENV !== 'production') {
    uni.showToast({
      title: 'An error occurred: ' + (err.message || 'Unknown error'),
      icon: 'none',
      duration: 3000
    });
  } else {
    // In production, show a generic message
    uni.showToast({
      title: 'An error occurred. Please try again.',
      icon: 'none',
      duration: 3000
    });
  }
};

// Add warning handler
app.config.warnHandler = function(msg, vm, trace) {
  console.warn('Vue warning:', msg);
  console.warn('Warning trace:', trace);
};
// #endif

// #ifdef VUE3
import { createSSRApp } from 'vue'
export function createApp() {
  const app = createSSRApp(App)
  
  // Add global error handler for Vue 3
  app.config.errorHandler = function(err, instance, info) {
    console.error('Global error:', err);
    console.error('Error info:', info);
    console.error('Error stack:', err && err.stack ? err.stack : 'No stack trace available');
    console.error('Browser info:', navigator.userAgent);
    
    // Check if it's a syntax error
    if (err instanceof SyntaxError) {
      console.error('SyntaxError detected. This might be due to unsupported JavaScript features in this browser.');
    }
    
    // Show error to user in development
    if (process.env.NODE_ENV !== 'production') {
      uni.showToast({
        title: 'An error occurred: ' + (err && err.message ? err.message : 'Unknown error'),
        icon: 'none',
        duration: 3000
      });
    } else {
      // In production, show a generic message
      uni.showToast({
        title: 'An error occurred. Please try again.',
        icon: 'none',
        duration: 3000
      });
    }
  };
  
  return {
    app
  }
}
// #endif
