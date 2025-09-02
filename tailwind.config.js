/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Penguin Ice Theme - Black & Blue
        'penguin-black': '#1a1a1a',      // Deep black background
        'penguin-charcoal': '#2d2d2d',   // Slightly lighter for cards
        'penguin-dark-gray': '#404040',  // Medium grey for borders
        'penguin-ice-blue': '#93C4D8',   // Ice blue accent color
        'penguin-ice-blue-dark': '#6BA3BF', // Darker ice blue
        'penguin-white': '#ffffff',      // Pure white
        'penguin-light-gray': '#f8fafc',
        
        // Card Color Variations - Cool ice theme
        'card-ice-blue': '#93C4D8',      // Ice blue
        'card-arctic-mint': '#A8E6CF',   // Mint green  
        'card-snow-purple': '#C8B6F6',   // Light purple
        'card-glacier-teal': '#81D4E3',  // Teal
        'card-frost-pink': '#FFB3D9',    // Pink
        
        // Legacy colors for compatibility
        'primary-green': '#7AB857',      // Original green
        'accent-yellow': '#FCE3AB',      // Light yellow accent
        'card-pink': '#FFB3D9',          // Pink
        'card-blue': '#93C4D8',          // Ice blue  
        'card-yellow': '#FCE3AB',        // Light yellow
        'text-dark': '#1a1a1a',          // Dark text
        'link-blue': '#93C4D8'           // Ice blue links
      },
      fontFamily: {
        'sans': ['-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'Inter', 'Helvetica Neue', 'Arial', 'sans-serif'],
        'display': ['-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'Inter', 'Helvetica Neue', 'Arial', 'sans-serif']
      },
      maxWidth: {
        'container': '1200px'
      }
    },
  },
  plugins: [],
}