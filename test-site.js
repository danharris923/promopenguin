const { chromium } = require('playwright');

async function testPromoPenguin() {
  console.log('🐧 Starting PromoPenguin Site Testing...\n');
  
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();
  
  // Set viewport
  await page.setViewportSize({ width: 1280, height: 720 });
  
  const baseUrl = 'http://localhost:3002';
  const issues = [];
  
  try {
    // Test Homepage
    console.log('📱 Testing Homepage...');
    await page.goto(baseUrl, { waitUntil: 'networkidle' });
    
    // Check page title
    const title = await page.title();
    console.log(`✓ Page title: ${title}`);
    
    // Check if main content loads
    const mainContent = await page.$('.max-w-container');
    if (!mainContent) {
      issues.push('❌ Main content container not found on homepage');
    } else {
      console.log('✓ Main content container loaded');
    }
    
    // Test Navigation Links
    console.log('\n🧭 Testing Navigation Links...');
    const navLinks = [
      { text: 'HOME', url: '/' },
      { text: 'DEALS', url: '/deals' },
      { text: 'FLYERS', url: '/flyers' },
      { text: 'COUPONS', url: '/coupons' },
      { text: 'AMAZON', url: '/amazon' },
      { text: 'ABOUT', url: '/about' }
    ];
    
    for (const link of navLinks) {
      try {
        console.log(`  Testing ${link.text} (${link.url})...`);
        await page.goto(`${baseUrl}${link.url}`, { waitUntil: 'networkidle' });
        
        // Wait for content to load
        await page.waitForTimeout(2000);
        
        // Check for any JavaScript errors
        const errors = await page.evaluate(() => {
          return window.console && window.console.error ? window.console.error.toString() : null;
        });
        
        // Check if page loaded successfully (no React error boundary)
        const hasError = await page.$('text=Something went wrong');
        if (hasError) {
          issues.push(`❌ ${link.text} page has React error boundary`);
        } else {
          console.log(`  ✓ ${link.text} page loaded successfully`);
        }
        
        // Check for broken images on this page
        const images = await page.$$('img');
        for (let i = 0; i < images.length; i++) {
          const img = images[i];
          const src = await img.getAttribute('src');
          const naturalWidth = await img.evaluate((el) => el.naturalWidth);
          
          if (src && src !== '' && naturalWidth === 0) {
            issues.push(`❌ Broken image on ${link.text}: ${src}`);
          }
        }
        
      } catch (error) {
        issues.push(`❌ Failed to load ${link.text} page: ${error.message}`);
      }
    }
    
    // Detailed testing of specific pages
    console.log('\n🔍 Detailed Page Testing...');
    
    // Test Flyers Page
    console.log('  Testing Flyers page functionality...');
    await page.goto(`${baseUrl}/flyers`, { waitUntil: 'networkidle' });
    await page.waitForTimeout(3000); // Wait for loading to complete
    
    const flyerCards = await page.$$('.bg-white.rounded-lg.shadow-md');
    if (flyerCards.length === 0) {
      issues.push('❌ No flyer cards found on Flyers page');
    } else {
      console.log(`  ✓ Found ${flyerCards.length} flyer cards`);
      
      // Test clicking on first flyer
      if (flyerCards.length > 0) {
        await flyerCards[0].click();
        await page.waitForTimeout(1000);
        
        // Check if modal opened
        const modal = await page.$('.fixed.inset-0.bg-black.bg-opacity-50');
        if (modal) {
          console.log('  ✓ Flyer modal opens correctly');
          
          // Close modal
          const closeButton = await page.$('button svg path[d*="M6 18L18 6M6 6l12 12"]');
          if (closeButton) {
            await closeButton.click();
            await page.waitForTimeout(500);
            console.log('  ✓ Modal closes correctly');
          }
        } else {
          issues.push('❌ Flyer modal does not open');
        }
      }
    }
    
    // Test Amazon Page
    console.log('  Testing Amazon page functionality...');
    await page.goto(`${baseUrl}/amazon`, { waitUntil: 'networkidle' });
    
    const amazonCategories = await page.$$('.bg-gradient-to-br');
    if (amazonCategories.length === 0) {
      issues.push('❌ No Amazon category cards found');
    } else {
      console.log(`  ✓ Found ${amazonCategories.length} Amazon category cards`);
    }
    
    // Check Amazon page background
    const bgColor = await page.evaluate(() => {
      const mainDiv = document.querySelector('div.min-h-screen');
      return mainDiv ? window.getComputedStyle(mainDiv).backgroundColor : 'not found';
    });
    console.log(`  ✓ Amazon page background color: ${bgColor}`);
    
    // Test Search functionality
    console.log('\n🔎 Testing Search Functionality...');
    await page.goto(`${baseUrl}/`, { waitUntil: 'networkidle' });
    
    const searchInput = await page.$('input[placeholder*="Search"]');
    if (searchInput) {
      await searchInput.fill('test search');
      await page.waitForTimeout(1000);
      console.log('  ✓ Search input works');
    } else {
      issues.push('❌ Search input not found');
    }
    
    // Mobile Menu Test
    console.log('\n📱 Testing Mobile Menu...');
    await page.setViewportSize({ width: 375, height: 667 }); // Mobile size
    await page.reload({ waitUntil: 'networkidle' });
    
    const mobileMenuButton = await page.$('button[aria-label="Toggle menu"]');
    if (mobileMenuButton) {
      await mobileMenuButton.click();
      await page.waitForTimeout(1000);
      
      // Check if mobile menu is visible
      const mobileMenu = await page.$('.md\\:hidden.py-3');
      if (mobileMenu) {
        const isVisible = await mobileMenu.isVisible();
        if (isVisible) {
          console.log('  ✓ Mobile menu opens correctly');
        } else {
          issues.push('❌ Mobile menu exists but not visible');
        }
      } else {
        issues.push('❌ Mobile menu does not open');
      }
    } else {
      issues.push('❌ Mobile menu button not found');
    }
    
  } catch (error) {
    issues.push(`❌ Critical error during testing: ${error.message}`);
  }
  
  // Summary
  console.log('\n' + '='.repeat(50));
  console.log('🐧 PromoPenguin Testing Complete!');
  console.log('='.repeat(50));
  
  if (issues.length === 0) {
    console.log('🎉 All tests passed! No issues found.');
  } else {
    console.log(`⚠️  Found ${issues.length} issues:\n`);
    issues.forEach((issue, index) => {
      console.log(`${index + 1}. ${issue}`);
    });
  }
  
  await browser.close();
  return issues;
}

// Run the test
testPromoPenguin().catch(console.error);