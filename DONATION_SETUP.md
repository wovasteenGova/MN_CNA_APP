# 💰 Donation Setup Instructions

## How to Update Your Donation Links

To customize the donation links with your actual accounts, edit the `openDonationLink` function in `pages/donate.vue`:

### Current Location (around line 85):
```javascript
const openDonationLink = (platform) => {
  // You can replace these with your actual donation links
  const donationLinks = {
    paypal: 'https://paypal.me/yourusername', // Replace with your PayPal.me link
    venmo: 'https://venmo.com/u/yourusername', // Replace with your Venmo username
    cashapp: 'https://cash.app/$yourusername'  // Replace with your Cash App username
  }
  // ... rest of function
}
```

### How to Get Your Links:

#### PayPal:
1. Go to [paypal.me](https://paypal.me)
2. Create your custom PayPal.me link
3. Replace `yourusername` with your actual PayPal.me handle
4. Example: `https://paypal.me/johndoe`

#### Venmo:
1. Open Venmo app or go to [venmo.com](https://venmo.com)
2. Find your Venmo username in your profile
3. Replace `yourusername` with your actual Venmo username
4. Example: `https://venmo.com/u/john-doe`

#### Cash App:
1. Open Cash App
2. Find your $Cashtag in your profile
3. Replace `yourusername` with your actual $Cashtag (without the $)
4. Example: `https://cash.app/$johndoe`

### After Making Changes:
1. Run `npm run generate` to rebuild the app
2. Deploy to Netlify

## 🎨 Customization Options

You can also:
- Change the donation button color by modifying the `color="amber"` attribute
- Add more payment platforms by adding them to the grid
- Modify the donation message text
- Add specific donation amounts or goals

## 📱 Mobile Optimized
The donation modal is fully responsive and works great on all devices!
