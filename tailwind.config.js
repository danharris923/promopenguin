/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // 808 Drum Machine-inspired colors (solid, no gradients)
        'penguin-black': '#2a2a2a',      // Dark charcoal background
        'penguin-charcoal': '#1a1a1a',   // Darker for cards/sections
        'penguin-dark-gray': '#3a3a3a',  // Medium grey
        'penguin-ice-blue': '#FF6B35',   // Bright red-orange
        'penguin-ice-blue-dark': '#E53E3E', // Bright red
        'penguin-white': '#ffffff',      // Pure white
        'penguin-light-gray': '#f8fafc',
        
        // 808 Card Color Variations 
        'card-ice-blue': '#FF6B35',      // Bright red-orange
        'card-arctic-mint': '#FFD700',   // Bright yellow  
        'card-snow-purple': '#E53E3E',   // Bright red
        'card-glacier-teal': '#FF8A65',  // Orange
        'card-frost-pink': '#ffffff',    // White
        
        // Legacy colors updated to 808 theme
        'primary-green': '#FF6B35',      // Red-orange primary
        'accent-yellow': '#FFD700',      // Bright yellow accent
        'card-pink': '#E53E3E',          // Red
        'card-blue': '#FF6B35',          // Red-orange  
        'card-yellow': '#FFD700',        // Bright yellow
        'text-dark': '#ffffff',          // White text
        'link-blue': '#FF6B35'           // Red-orange links
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