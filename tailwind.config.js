/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Penguin Dark Theme Colors
        'penguin-black': '#0a0a0a',
        'penguin-charcoal': '#1a1a1a',
        'penguin-dark-gray': '#2a2a2a',
        'penguin-ice-blue': '#7dd3fc',
        'penguin-ice-blue-dark': '#0284c7',
        'penguin-white': '#ffffff',
        'penguin-light-gray': '#f8fafc',
        
        // Card Color Variations (Penguin-inspired)
        'card-ice-blue': '#bfdbfe',
        'card-arctic-mint': '#a7f3d0',
        'card-snow-purple': '#ddd6fe',
        'card-glacier-teal': '#99f6e4',
        'card-frost-pink': '#fce7f3',
        
        // Legacy colors for migration compatibility
        'primary-green': '#7AB857',
        'accent-yellow': '#FCD144',
        'card-pink': '#EAB2AB',
        'card-blue': '#93C4D8',
        'card-yellow': '#FCE3AB',
        'text-dark': '#333333',
        'link-blue': '#0074DB'
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